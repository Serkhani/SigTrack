import json
import requests
import machineid
from sigtrack.models.image_models.watermarkitem import logger

CONTEXT = {
  "KEYGEN_ACCOUNT_ID": 'e5dd220a-911b-4cad-b8d1-6192f770f8fb'
}

def activateLicense() -> bool:

  try:
    # Read the license key from the file
    with open("license.key", "r") as file:
        licenseKey = file.read().strip()  # Strip whitespace and newlines
  except FileNotFoundError:
    return False, 'No license key file found'

  machineFingerprint = machineid.hashed_id('Sigtrack')
  validation = requests.post(
    "https://api.keygen.sh/v1/accounts/{}/licenses/actions/validate-key".format(CONTEXT['KEYGEN_ACCOUNT_ID']),
    headers={
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json"
    },
    data=json.dumps({
      "meta": {
        "scope": { "fingerprint": machineFingerprint },
        "key": licenseKey
      }
    })
  ).json()

  if "errors" in validation:
    errs = validation["errors"]

    return False, "license validation failed: {}".format(
      ','.join(map(lambda e: "{} - {}".format(e["title"], e["detail"]).lower(), errs))
    )

  # If the license is valid for the current machine, that means it has
  # already been activated. We can return early.
  if validation["meta"]["valid"]:
    return True, "license has already been activated on this machine"

  # Otherwise, we need to determine why the current license is not valid,
  # because in our case it may be invalid because another machine has
  # already been activated, or it may be invalid because it doesn't
  # have any activated machines associated with it yet and in that case
  # we'll need to activate one.
  validationCode = validation["meta"]["code"]
  requiresActivation = validationCode == 'FINGERPRINT_SCOPE_MISMATCH' or \
                          validationCode == 'NO_MACHINES' or \
                          validationCode == 'NO_MACHINE'

  if not requiresActivation:
    return False, "license {}".format(validation["meta"]["detail"])

  # If we've gotten this far, then our license has not been activated yet,
  # so we should go ahead and activate the current machine.
  activation = requests.post(
    "https://api.keygen.sh/v1/accounts/{}/machines".format(CONTEXT['KEYGEN_ACCOUNT_ID']),
    headers={
      "Authorization": "License {}".format(licenseKey),
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json"
    },
    data=json.dumps({
      "data": {
        "type": "machines",
        "attributes": {
          "fingerprint": machineFingerprint
        },
        "relationships": {
          "license": {
            "data": { "type": "licenses", "id": validation["data"]["id"] }
          }
        }
      }
    })
  ).json()

  # If we get back an error, our activation failed.
  if "errors" in activation:
    errs = activation["errors"]

    return False, "license activation failed: {}".format(
      ','.join(map(lambda e: "{} - {}".format(e["title"], e["detail"]).lower(), errs))
    )

  return True, "license activated"
