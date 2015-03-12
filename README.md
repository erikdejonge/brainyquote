# brainyquotesdownloader
Downloads all quotes from http://www.brainyquote.com
##run
```bash
python printbrainyquote.py -f inspirational
python printbrainyquote.py -f technology
```

##build
```bash
python brainyquotesdownloader.py
cd quotes
python sanitize.py
python bundle.py
python sanitize.py
cd ..
python makealldats.py
```