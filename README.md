How to run this program:
========================

- make sure you have Vagrant and VirtualBox installed on your machine
- navigate to the project directory in your command line
- in order to initialize a Vagrant environment, type the
  command: 'vagrant init'
- now type the command 'vagrant up' to start the Vagrant environment
- login to the Vagrant machine using the command:'vagrant ssh'
- now that you're logged in, navigate back to the project directory
  in your new Vagrant environment using the command: 'cd /vagrant'
- cd back into the 'tournament' project directory
- run the SQL commands in the file 'tournament.sql' inside
  the postgresql command line prompt by typing the command:
  'psql -f tournament.sql'
- you are now finally ready to test the code in the file
  'tournament.py'.  to do this, run the tests in the file
  'tournament_test.py' by typing the command: 'python tournament_test.py'
