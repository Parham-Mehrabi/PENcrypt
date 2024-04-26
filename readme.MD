# PENCrypt

this is a simple project where you can hide your sensitive data somewhere secure

example of uses:
-
- storing a __file for passwords__ locally
- storing __details of your wallet__ locally
- a local __diary__, you can keep your memories somewhere safely


why is it safe?
- 
- its open source you can check how is it working in its repo
- it does not store your passwords it just store the salt and iterations
- its impossible to brute force your password since it iterate the hashing process for 700k times which take like 1 sec to create a key to unlock data
- its offline(so far) and its all on your own machine


---
im planing to move the GUI to a web version and change the backend to Rust-lang soon, feel free if you want to contribute