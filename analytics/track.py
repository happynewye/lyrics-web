class Track(object):
    def request(self, request, dt):
        print(request.url, 1000 * dt)

    def event(self, request, event):
        print(event)
