## Lab 1: Restoring the Web Server

Oh no! The company's web server has been taken down. Due to a failure of the organization to patch systems and rotate ssh keys, you are about to have a very, very bad day. Our website has been defaced, with our investors coming in on Tuesday, we need to remediate this right now. I don't have a backup of the web content, but I know that there are plenty of half-finished projects just sitting around the web server.

## Objective

<ol id="list">
<li>SSH into the server</li>
<li>Navigate to the directory serving the defaced web page</li>
<li>Copy the corrupted file into an evidence folder</li>
<li>Delete the corrupted file</li>
<li>Create a new file to be served by the webpage</li>
<li>Build a new Under Construction page</li>
</ol>