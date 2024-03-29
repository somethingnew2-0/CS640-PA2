CS640-PA2
=========

Created by: Peter Collins (pcollins) & Cory Groom (groom)

#Mininet and Bufferbloat

##Background

Software Defined Networking (SND) has emerged over the past several years as a compelling new technology for managing networks – primarily in the local area and in data centers.  The crux of SDN is that it provides network administrators with the ability to flexibly control where traffic flows in a switched environment.  This is done by adding a control plane and certain new capabilities for switching in the data plane in layer 2 devices.  This is quite different from standard layer 2 switches.  In SDN, control is typically assumed to be centralized i.e., it runs on a system that is separate from the switches themselves (referred to as the controller).  This offers certain advantages in terms of algorithms that might be used to manage/control the data plane in switches.  The controller communicates with the switches using a specialized protocol.  One protocol that has been standardized for this purpose is called OpenFlow.  The original paper that describes OpenFlow can be found here.  A very nice overview of software defined networks can be found here. 

The Mininet environment was developed to help promote the development of software defined networks in general and OpenFlow in particular.  The original paper that describes Mininet can be found here.  In that paper, Mininet is described as a rapid prototyping environment for software defined networks.  It is similar to a network simulator, but with the advantage that it relies on the user to create test configurations using a language that is used to configure real systems.  It enables a wide variety of network configurations to be tested and evaluated on a single system instead of having to have a bunch of real OpenFlow-enabled switching hardware.  In fact, Mininet is so flexible and convenient, that it can be used for fairly general kinds of experiments such as classroom projects.

Finally, as we have discussed in class, buffers play an important role in statistically multiplexed packet switched networks.  Specifically, they are deployed in routers and switches to absorb bursts of packet that may arrive at a switch.  Since packet loss is a standard performance metric in service level agreements, providers typically configure their systems with buffers that are equal to the delay x bandwidth of a link.  This rule-of-thumb is commonly ascribed to a 1994 paper by Villamizer and Song, which can be found here.  However, in recent years, the broad deployment of large buffers in devices throughout the Internet has led to a conversation about the risks of very long delays that might be inflicted on packets.  This issue is generally referred to as bufferbloat.  A site devoted to this issue can be found here. 

##Description

For this assignment you will become familiar with Mininet and use it to conduct simple experiments on the problem of bufferbloat.  The lab will also give you some experience with the Python programming language and may also give you a little bit of experience with other tools and systems such as Github and virtual machines depending on how you decide to proceed with your experiments.

To run Mininet, you need a virtual machine.  There are many VM’s available from vendors, many of which are free.  Oracle’s VirtualBox is available in the mumble lab.  We also have the Instructional Virtual Lab, which runs on VMware.  You are welcome to conduct you experiments on your personal systems, but for the purpose of the demo, you will need to run in the Instructional Virtual Lab.
To use the Instructional Virtual Lab, you must request it access using the form that can be found here. You simply need to mention that you want the Mininet template, who is on your team and then CSL set up a VM.  Further documentation is located here.   If you are setting up Mininet on your own systems, you can find instructions on how to do so here.
 
After you have Mininet running, you will begin by doing the standard walkthrough of the system – instructions can be found here.  Note that at the top of this set of instructions, it says that it should only take about an hour to complete these exercises.  However, it will be important for you to pay particular attention to how to create topologies, how to test connectivity in topologies and how to capture data for further analysis.  Next, to give you a more detail on Mininet commands go through the Mininet introduction, which can be found here.   While it is not required, you can get even more experience by going through the OpenFlow tutorial, which can be found here.  You can also find examples of other Mininet
 
Upon completion of the Mininet walkthrough and introduction, you can proceed with the lab on bufferbloat.  The lab description can be found here.
