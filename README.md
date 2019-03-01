# Trellis+P4 Tutorial

Welcome to the Trellis+P4 tutorial! The goal of this tutorial is to learn how to
use Trellis to control a leaf-spine fabric of P4-capable devices using ONOS, and
how you can use `fabric.p4` (the reference P4 program used by Trellis) to
perform advanced packet processing such as VNF offloading.

## Slides

Tutorial slides can be downloaded at <http://bit.ly/trellis-p4-slides>

## Tutorial VM

To complete the exercises, you will need to download and run the tutorial VM.
The instruction of downloading and setting up the tutorial VM can be found at <http://bit.ly/trellis-p4-vm-instructions>

To run the VM you can use any modern virtualization system, although we
recommend using VirtualBox. To download VirtualBox and import the VM use the
following links:

* <https://www.virtualbox.org/wiki/Downloads>
* <https://docs.oracle.com/cd/E26217_01/E26796/html/qs-import-vm.html>

### VM credentials

The VM comes with one user with sudo privileges. Use these credentials to log in:

* Username: `sdn`
* Password: `rocks`

## ONOS version

This tutorial is based on the development branch of ONOS version 1.14:
<https://github.com/opennetworkinglab/onos/tree/onos-1.14>

## Overview

Before starting, we suggest to open the `trellis-p4-tutorial` directory
in your editor of choice for easier access to the different files used in the
exercises. For example, if using the Atom editor:

```
$ atom ~/trellis-p4-tutorial
```

### fabric.p4

These exercises are based on `fabric.p4`, the P4 implementation of the reference
Trellis data plane pipeline. The source code of fabric.p4 and its ONOS pipeconf
implementation can be found here:
<https://github.com/opennetworkinglab/onos/tree/onos-1.14/pipelines/fabric>.

Some useful files are:

* [fabric.p4](https://github.com/opennetworkinglab/onos/blob/onos-1.14/pipelines/fabric/src/main/resources/fabric.p4):
Top level file of the P4 implementation.

* [Makefile](https://github.com/opennetworkinglab/onos/blob/onos-1.14/pipelines/fabric/src/main/resources/Makefile):
Used to compile the different profiles of `fabric.p4`, such as `fabric-spgw`,
`fabric-int`, etc. This file specifies the preprocessor flags used by the P4
compiler for each profile.

* [spgw.p4](https://github.com/opennetworkinglab/onos/blob/onos-1.14/pipelines/fabric/src/main/resources/include/spgw.p4):
P4 implementation for the S/PGW functionality integrated in the `fabric-spgw`
profile. This implementation provides the tables and actions to perform GTP
encapsulation and decapsulation.

* [Pipeconf Java implementation](https://github.com/opennetworkinglab/onos/tree/onos-1.14/pipelines/fabric/src/main/java/org/onosproject/pipelines/fabric):
Here is where we implement, among other things, the Pipeliner, which is the ONOS
driver behavior providing the logic to translate the Trellis FlowObjectives to
the FlowRules specific to the `fabric.p4` pipeline.

## Tutorial exercises

### Lab 1

[Click here to go to this exercise instructions](lab1/README.md)

This exercise shows how to set up an emulated Trellis environment with a simple
2x2 topology of BMv2 software switches programmed with the basic `fabric`
profile. In this exercise, you will have to modify the network configuration
file (netcfg) to add a new interface and provide connectivity for a new host.

### Exercise 2

[Click here to go to this exercise instructions](lab2/README.md)

This exercise shows how to use and control the S/PGW functionality integrated in
the `fabric-spgw` profile to encapsulate packets using the GTP header directly
in the switch.
