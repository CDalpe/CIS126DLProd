## Scenario

Oh no! The company's web server has been taken down. Due to a failure of the organization to patch systems and rotate ssh keys, you are about to have a very, very bad day. Our website has been defaced, with our investors coming in on Tuesday, we need to remediate this right now. I don't have a backup of all the web content, but I know that there are plenty of half-finished projects just sitting around the web server, maybe we can use the under construction page from back before we completed the website?

## Objectives

<ol id="list">
<li>SSH into the server</li>
<li>Navigate to the directory serving the defaced web page</li>
<li>Copy the corrupted file into an evidence folder</li>
<li>Delete the corrupted file</li>
<li>Create a new file to be served by the webpage</li>
<li>Build a new Under Construction page</li>
</ol>

## Background

First, let's check what the attacker left on our web server. Navigate to <a href="http://192.168.56.20" target="_blank" rel="noopener noreferrer" aria-label="View company web server (opens in new window)">your company's web server</a>

*What did you notice?* Do you think that is what a real company would expect to have on their website? Probably Not.

Second, let's make sure that we still have access to the server machine. 

```bash
vagrant ssh server-vm
```

Why this works. Secure Shell (ssh) is a common network protocol that is a staple of the Linux CLI management paradigm. Since most Linux boxes don't traditionally install a GUI, since it takes resources that could be more valuably used elsewhere. Vagrant does us a favor by managing these sessions and keys for us, though if we wanted we could export that key and import it into a free terminal/ssh manager platform like <a href="https://putty.org" target="_blank" rel="noopener noreferrer" aria-label="navigate to PuTTy homepage">PuTTy</a>, or <a href="https://mremoteng.org/" target="_blank" rel="noopener noreferrer" aria-label="navigate to mRemoteNG homepage">mRemoteNG</a>.

### The Linux Terminal/Shell

When we first log into the operating system it should look like this

```bash
[vagrant@server-vm ~]$
```

This tells us *user*@**location** - or who we are and on what machine we are currently working. This becomes vital information when working in larger complex environments where an administrator has access to multiple user or service accounts across hundreds or thousands of machines. The program used to type commands is called the *terminal*. Terminals traditionally have black or white backgrounds but can be configured as the user finds appropriate or necessary (for accessibility concerns). This window is what a user will type into, and will display the output of those commands. When a user enters a command, the *shell* is what takes that information and relays to the *kernel* the sets of instructions that the user has requested, such as moving their current location, opening a file, or running software/utilities.

### File Hierarchy and Navigating the OS

When a user first logs into a system they don't understand, they need to perform some basic recon. What is the system? What does it do? Where am I in its *File Hierarchy Structure* or FHS. The current location of the user's session is called the *Working Directory*, and to understand the user's absolute location in the FHS we use the command:

```bash
pwd
```

or *print working directory*. Do that now and check where you login sessions land you.

Moving through the operating system is as fundamental a skill as can be asked of any administrator. To understand how to move through the OS, we should start with understanding how our shell interprets our commands. The developers behind the Linux shell interpreter have decided that the structure they will use is:

```bash
command *options*
```

Utilities and software can come with options that change the behavior of the utility, or input to it some required or optional information for it to perform. There is no hard and fast rule requiring that commands to the shell be provided in this way, and anyone is free to write a shell interpreter that changes this structure. But that is the world of computers, there are traditions on which we build guidelines, but if enough people break those traditions we can form entirely new ones (more on this when we discuss RFCs).

This lab has seven (7) basic commands that are foundational to your experience with Linux:
<table>
    <caption>Common Linux Commands</caption>
    <thead>
        <tr>
            <th scope="col">Command</th>
            <th scope="col">Purpose</th>
            <th scope="col">Common Options</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th scope="row">pwd</th>
            <td>Print Working Directory</td>
            <td>-L --lists logical directory<br>-P --lists physical (absolute) directory</td>
        </tr>
        <tr>
            <th scope="row">cd</th>
            <td>Change Directory</td>
            <td>".." -- up one level<br>"../.." --up two levels (and so on)<br>You can also call absolute or relative paths</td>
        </tr>
        <tr>
            <th scope="row">ls</th>
            <td>List</td>
            <td>-a -- all<br>-d --directory<br>-l --long list</td>
        </tr>
        <tr>
            <th scope="row">cp</th>
            <td>Copy</td>
            <td></td>
        </tr>
        <tr>
            <th scope="row">rm</th>
            <td>Remove</td>
            <td>-f --force<br>-r --recursive<br>-d --directory</td>
        </tr>
        <tr>
            <th scope="row">touch</th>
            <td>Create or Refresh File</td>
            <td></td>
        </tr>
        <tr>
            <th scope="row">man</th>
            <td>Manual Pages</td>
            <td></td>
        </tr>
    </tbody>
</table>

This is by no means an exhaustive list, even for this class. We will cover more commands and in more depth in future chapters. For now, these will suffice for our purposes.

### Special Considerations - man Pages

Prior to the widespread usage of World Wide Web (WWW) in the 1990s, developers needed a method to communicate how the libraries or utilities they wrote could be used. Today, we have the Internet. The popular methodology was to use the *man pages*, short for manual. These are written by the developer to instruct other users on the syntax and command switches of the utility that they wrote. This should be your first stop if you aren't getting the results that you expect (example shown for *pwd*):

```bash
[vagrant@server-vm ~]$ man pwd
```
 or 

```bash
[vagrant@server-vm ~]$ pwd --help
```

## Instructions
<br>

### Objective 1 - SSH into the web server

This was completed as part of the background

### Objective 2 - Navigate to the defaced web directory

Now that we know we have access to the server. We need to first remove the defaced website from being advertised to our clients, customers, and internal stakeholders. Everyone knows that we got hit by malware, no need to advertise it further. By default, Apache (web server software) hosts the homepage for a web server at:

```bash
/var/www/html/index.html
```

But the file is located *inside* the directory, so we don't need to call the whole file, only the directory in which it is contained (*leave off the index.html*). If you call the absolute using change directory, Linux should be able to navigate directly to it. 

### Objective 3 - Copy the Corrupt File into Evidence

This is not something one would realistically do during an incident, admittedly. During an incident the first step would be to capture a forensic image, we would not back up the evidence to a file on the device. We would capture a forensic image before doing anything else so as to preserve the evidence for a future post-mortem report to stakeholders. Since incident response is outside the scope of this class, we can safely notionalize that copying the file into an evidence folder is creating a forensic image. 

Using the *cp* command, copy the *index.html* file from its place in **/var/www/html/** to /home/evidence

```bash
cp <source> <destination>
```

### Objective 4 - Delete the Corrupted Webfile

Using the *rm* command, delete the *index.html* that exists in **/var/www/html/**.

### Objective 5 - Create a New Index File

Using the *touch* command, create a new *index.html*

### Objective 6 - Paste New Content into Index

From the **/backups/website/** directory, copy the file from *index.html* into **/var/www/html/**. Then navigate to **/var/www/html** and open the file using vim or nano:

```bash
nano index.html
```

or 

```bash
vim index.html
```

To verify the content is what you expect.

## Submission

Once that is complete click the **Grade Lab** button below to verify your work. You will receive a score and a hash value (a string of numbers or letters). Copy and paste the hash value exactly into the LMS.