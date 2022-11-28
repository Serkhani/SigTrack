function onLoad() {
    console.log("onLoad start==================")

    ice.enqueue('#test', function test() {
        console.log('!!!! RAN ME TO ANONYMOUSE')
    })
    ice.enqueue('#asdft', function newtest(reply) {
        console.log('!!!! PASS DATA:    ' + reply + "\n")
    })
    console.log("     =========================")
    ice.processResponses()
    console.log("onLoad done==================")
}

function hi() {
    ice.showImage()
}
