
INSERT INTO `domains` (id,name,master,last_check,type,notified_serial,account) VALUES (1,'test.com',NULL,NULL,'NATIVE',NULL,NULL);
INSERT INTO `domains` (id,name,master,last_check,type,notified_serial,account) VALUES (2,'97.168.192.in-addr.arpa',NULL,NULL,'NATIVE',NULL,NULL);

INSERT INTO `records` (domain_id,name,type,content,ttl,prio,change_date) VALUES (1,'test.com','SOA','localhost ahu@ds9a.nl 1',86400,NULL,NULL);
INSERT INTO `records` (domain_id,name,type,content,ttl,prio,change_date) VALUES (1,'test.com','NS','dns-us1.powerdns.net',86400,NULL,NULL);
INSERT INTO `records` (domain_id,name,type,content,ttl,prio,change_date) VALUES (1,'test.com','NS','dns-eu1.powerdns.net',86400,NULL,NULL);

INSERT INTO `records` (domain_id,name,type,content,ttl,prio,change_date) VALUES (2,'97.168.192.in-addr.arpa','SOA','localhost ahu@ds9a.nl 1',86400,NULL,NULL);
INSERT INTO `records` (domain_id,name,type,content,ttl,prio,change_date) VALUES (2,'97.168.192.in-addr.arpa','NS','dns-us1.powerdns.net',86400,NULL,NULL);
INSERT INTO `records` (domain_id,name,type,content,ttl,prio,change_date) VALUES (2,'97.168.192.in-addr.arpa','NS','dns-eu1.powerdns.net',86400,NULL,NULL);

