# This script tracks [this](https://www.airpaq.de/collections/alle-produkte/products/turnbeutel-baq?variant=40697128321135) item for availability
And sends an E-Mail if the status of the item has changed

## Setup
Clone the repo:
```bash
git clone https://github.com/ruarq/BaqTracker.git
```

Setup your E-Mail:
```bash
cd BaqTracker
touch .env
```

Use your favorite editor to edit the `.env` file you just created and fill it with the following contents:
```env
EMAIL_HOST=<your smtp host (i.e. mail.example.com / smtp.gmail.com)>
EMAIL_PORT=<your smtp port (465 for SSL)>
EMAIL_ADDRESS=<your email>
EMAIL_PASSWORD=<your email password>

RECIPIENT_NAME=<the recipients name>
RECIPIENT_MAIL=<the recipients email>
```
NOTE: There are a few problems when it comes to using @gmail.com addresses to send the mails (you can try it, it may work),
but you probably will get an email from Google telling you someone tried to login to your gmail account.

There are other ways of notifying you when the status has changed, you just have to set them up yourself.
Just edit the `notify` function in the `status_changed.py` file to do whatever you want.
Make your computer beep, send a discord message or launch a nuclear missile. Whatever you want.

### Extra
If you want to run the program automatically on your machine, you can run the `crontab.sh` script to setup a cron job automatically.
It will set it up so that the script runs from monday to friday at 8am and at 6pm.
