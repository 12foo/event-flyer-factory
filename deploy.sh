#!/bin/bash
ssh uwsgi@flyers.forbernie.com /bin/bash << EOF
    source /uwsgi/envs/event-flyer-factory/bin/activate
    cd /uwsgi/apps/event-flyer-factory
    git pull
    pip install -r requirements.txt
    rm -f /uwsgi/apps/event-flyer-factory/previews/*.png
    uwsgi --reload /uwsgi/event-flyer-factory.pid
EOF

