# ADR2 - Web Sockets vs Long Polling

Date: 14/05/2024

Status: Accepted

# Summary

The team decided to use long polling to connect the server and the client instead of web sockets. We made this decision as it was less complex to integrate the degree of security we wanted with long polling than web sockets.

# Context

The proposal called for secure, low latency, instant messaging. We had two options of connecting the client and server, long polling and web sockets, each with their own pros and cons. 

* The team was more familiar with integrating security for long polling than web sockets. Security is the most important ASR.
* Web sockets have very low latency. This is key for instant messaging.
* Web sockets are more efficient and scalable.
* There are many deliverables other than the program itself (testing, documentation, video) and they are weighted more in the criteria.

# Decision

The team decided to go with long polling to connect the client and server. 

# Consequences

Using long polling will ensure that we will be able to integrate the level of security we want in the given time frame. We need to finish the programming exaclty on time so we can begin working on the other deliverables which are worth more marks than the programming. However, long polling has higher latency, lower efficiency and is less scalable than web sockets. However, as security is the most important ASR, we determined this trade-off to be acceptable. 

