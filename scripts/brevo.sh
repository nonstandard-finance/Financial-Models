curl --request POST \
  --url https://api.brevo.com/v3/smtp/email \
  --header 'accept: application/json' \
  --header 'api-key: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' \
  --header 'content-type: application/json' \
  --data '{
   "sender":{
      "name":"Sender Alex",
      "email":"omoebun52@gmail.com"
   },
   "to":[
      {
         "email":"omoebun52@gmail.com",
         "name":"John Doe"
      }
   ],
   "subject":"Hello world",
   "htmlContent":"<html><head></head><body><p>Hello,</p>This is my first transactional email sent from Brevo.</p></body></html>"
}'
