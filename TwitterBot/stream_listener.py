from tweepy import StreamListener

class TwitterListener(StreamListener):
 
    def on_status(self, status):
        print('%-25s:' % status.user.screen_name + status.text)
        return True
 
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True
 
    def on_timeout(self):
        print('Timeout...')
        return True
 
