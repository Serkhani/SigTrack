from sigtrack.models.video_models.marker.video_marker import VideoMarker
class  MarkerPopUpModel():
    def __init__(self):
        self.markers:list[VideoMarker] = []

    def addMarker(self):
        marker = VideoMarker()
        self.markers.append(marker)        