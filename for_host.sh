ufw allow ssh
ufw allow from 46.101.44.87 to any port 443,80 proto tcp
ufw enable 

echo "ScrapeOps server ip & port whitelisted using ufw"