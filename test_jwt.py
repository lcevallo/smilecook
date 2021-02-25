import base64

payload = 'eyJpYXQiOjE1NjQ5ODI5OTcsIm5iZiI6MTU2NDk4Mjk5NywianRpI joiMGIzOTVlODQtNjFjMy00NjM3LTkwMzYtZjgyZDgyYTllNzc5IiwiZXhwIjoxNTY0 OTgzODk3LCJpZGVudGl0eSI6MywiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0'

base64.b64decode(payload + '==')
print(base64.b64decode(payload + '=='))