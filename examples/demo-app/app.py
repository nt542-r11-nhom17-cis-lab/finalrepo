"""Local-only demo application. No network listener, credentials or third-party dependencies."""

def message():
    return 'CIS sandbox deployment succeeded'

if __name__ == '__main__':
    print(message())
