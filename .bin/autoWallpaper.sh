#!/bin/sh


export DISPLAY=:0
feh --randomize --bg-fill /home/edupin/.config/awesome/background/* >> /home/edupin/aaaaaaaa_last_update_wallpaper.txt

# crontab -e
# ou edn /var/spool/cron/edupin
# Set this inside:
#
# # Minute   Hour   Day of Month       Month          Day of Week        Command    
# # (0-59)  (0-23)     (1-31)    (1-12 or Jan-Dec)  (0-6 or Sun-Sat) 
#   */30     *          *             *                 *               /home/edupin/.bin/autoWallpaper.sh
#
