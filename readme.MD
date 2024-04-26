# PENCrypt

this is a simple project where you can hide your sensitive data somewhere secure

example of uses:
-
- storing a __passwords file__ locally
- storing your __wallet__ details locally
- a local __diary book__, you can keep your memories somewhere safely


why is it safe?
- 
- its open source you can check how is it working in its repo
- it does not store your passwords it just store the salt and iterations
- its impossible to brute force your password since it iterate the hashing process for 700k times which take like 1 sec to create a key to unlock data
- its offline(so far) and its all on your own machine
