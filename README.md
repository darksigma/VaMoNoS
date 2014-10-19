# VaMoNos - Vaccination Monitoring and Notification Service

This is our submission to Hacking Pediatrics! You can find a demo [here](https://www.youtube.com/watch?v=JGNLnXBIz4Q)!

## Need
In developing nations, many people aren't able to keep track of their child's immunizations. Hard copies of records are easily lost and there is no centralized location to retrieve this information. Moreover, there is little incentive to get children immunized when it is at the cost of losing hours in the workday when they could otherwise be earning money for their family.

## Solution
We've developed a system that allows parents to use text messaging to keep track of their child's immunizations. When their child is born, they are signed up for the service by sending the following command to +14088053907, the number associated with our Twilio application:

`reg name:Nikhil Buduma dob:2/29/2014 zipcode:02139`

At this point, the parents will be able to:
 1. text `record` to the database to retrieve information about their child's immunization status 
 2. text `send +12394956789` to securely send their child's record to a third party using TigerText with one view restrictions and a 30-day expiration date (the number listed should be repaced with the intended recipient's number) 
 3. text `email nkbuduma@mit.edu` to send their child's record to a trusted party using MailJet as a formatted email (the email listed should be repaced with the intended recipient's email)
 4. text an immunization code they would receive from their healthcare provider to update their record and receive free minutes as an incentive for immunizing their child. 

Moreover, we implement a notification service that notifies the parent via text message whenever their child is due for a vaccination. This reminder is sent weekly to the parent to make sure they get their child immunized. 
