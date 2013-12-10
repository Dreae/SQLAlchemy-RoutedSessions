RoutedSessions
================
This is just a simple package that allows you to use database replication with SQLAlchemy.
 With RoutedSessions you can define multiple master and slave database engines, all write 
actions will occur on one of the master engines, and all reads will occur on one of the slaves.