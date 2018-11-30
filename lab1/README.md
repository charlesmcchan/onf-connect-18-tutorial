# Trellis + P4 Tutorial: Lab 1 - Trellis Basics

The goal of this exercise is to learn how to setup an emulated Trellis environment with basic configurations.

To run this exercise you will need multiple terminal windows (or tabs) to
operate with the CLI of Mininet and ONOS. We use the following convention
to distinguish between commands of different CLIs:

* Commands starting with `$` are intended to be executed in the Ubuntu terminal
    prompt;
* `onos>` for commands in the ONOS CLI;
* `mininet>` for the Mininet CLI.

## Topology
![Topology|small](https://raw.githubusercontent.com/charlesmcchan/onf-connect-18-tutorial/master/lab1/topology.png)

## Exercise steps

1. On terminal window 1, **start ONOS with a set of the apps**
by executing the following command:

    ```
    $ cd $ONOS_ROOT
    $ ONOS_APPS=drivers,openflow,segmentrouting,drivers.bmv2,pipelines.fabric ok clean
    ```

    The `$ONOS_ROOT` environment variable points to the root ONOS directory. The
    `ok` command is an alias to run ONOS locally in your dev machine. Please
    note that if this the first time you run ONOS on this machine, or if you
    haven't built ONOS before, it can take some time (5-10 minutes depending on
    your Internet speed).

    Once ONOS has started you should see log messages being print on the screen.

2. On terminal window 2, **push network configuration to ONOS**.

    ```
    $ onos-netcfg localhost ~/onf-connect-18-tutorial/lab1/trellisp4.json
    ```

3. On terminal window 2, **open ONOS CLI to verify the system is up an running**.

    1. Use the following command to **access the ONOS CLI**:

        ```
        $ onos localhost
        ```

        You should now see the ONOS CLI command prompt. For a list of possible
        commands that you can use here, type:

        ```
        onos> help onos
        ```

    2. To **verify that you have activated all the required apps**, run the
        following command:

        ```
        onos> apps -a -s
        ```

        Make sure you see the following list of apps displayed:

        ```
        *   7 org.onosproject.route-service        1.14.2.SNAPSHOT Route Service Server
        *  14 org.onosproject.drivers              1.14.2.SNAPSHOT Default Drivers
        *  15 org.onosproject.optical-model        1.14.2.SNAPSHOT Optical Network Model
        *  29 org.onosproject.openflow-base        1.14.2.SNAPSHOT OpenFlow Base Provider
        *  30 org.onosproject.lldpprovider         1.14.2.SNAPSHOT LLDP Link Provider
        *  31 org.onosproject.hostprovider         1.14.2.SNAPSHOT Host Location Provider
        *  44 org.onosproject.protocols.grpc       1.14.2.SNAPSHOT gRPC Protocol Subsystem
        *  67 org.onosproject.protocols.p4runtime  1.14.2.SNAPSHOT P4Runtime Protocol Subsystem
        *  84 org.onosproject.protocols.gnmi       1.14.2.SNAPSHOT gNMI Protocol Subsystem
        *  91 org.onosproject.generaldeviceprovider 1.14.2.SNAPSHOT General Device Provider
        *  92 org.onosproject.drivers.gnmi         1.14.2.SNAPSHOT gNMI Drivers
        * 101 org.onosproject.openflow             1.14.2.SNAPSHOT OpenFlow Provider Suite
        * 114 org.onosproject.p4runtime            1.14.2.SNAPSHOT P4Runtime Provider
        * 115 org.onosproject.drivers.p4runtime    1.14.2.SNAPSHOT P4Runtime Drivers
        * 122 org.onosproject.mcast                1.14.2.SNAPSHOT Multicast traffic control
        * 123 org.onosproject.segmentrouting       1.14.2.SNAPSHOT Segment Routing
        * 132 org.onosproject.pipelines.basic      1.14.2.SNAPSHOT Basic Pipelines
        * 145 org.onosproject.pipelines.fabric     1.14.2.SNAPSHOT Fabric Pipeline
        * 167 org.onosproject.drivers.bmv2         1.14.2.SNAPSHOT BMv2 Drivers
        ```

    3. Enter the following command to **verify the network config**:

        ```
        onos> netcfg
        ```
        
        You should see 4 devices and 3 ports configured.

4. (optional) **Change flow rule polling interval**. Run the following
    command in the ONOS CLI:

    ```
    onos> cfg set org.onosproject.net.flow.impl.FlowRuleManager fallbackFlowPollFrequency 5
    ```

    This command tells ONOS to check the state of flow rules on switches
    every 5 seconds (default is 30). This is used to obtain more often flow
    rules stats such as byte/packet counters. It helps also resolving more
    quickly issues where some flow rules are installed in the ONOS store but
    not on the device (which can often happen when emulating a large number
    of devices in the same VM).

5. On terminal window 3, **run Mininet to set up a topology of BMv2 devices**.

    1. To **run Mininet**, use the following command:

        ```
        cd ~/onf-connect-18-tutorial/lab1
        sudo -E env PYTHONPATH=$PYTHONPATH:$ONOS_ROOT/tools/dev/mininet ./trellisp4.py --onos-ip 127.0.0.1
        ```

        The `--custom` argument tells Mininet to use the `bmv2.py` custom script
        to execute the BMv2 switch. The environment variable `$BMV2_MN_PY`
        points to the exact location of the script (you can use the command
        `echo $BMV2_MN_PY` to find out the location).

        The `--switch` argument specifies the kind of switch instance we want to
        run inside Mininet. In this case we are running a version of BMv2 that
        also produces some configuration files used by ONOS to discover the
        device (see steps below), hence the name `onosbmv2`. The `pipeconf`
        sub-argument is used to tell ONOS which pipeconf to deploy on all
        devices.

        The `--controller` argument specifies the address of the controller,
        ONOS in this case, which is running on the same machine where we are
        executing Mininet.

    2. A set of **files are generated in the `/tmp` folder as part of this
        startup process**, to view them (on a separate terminal window):

        ```
        $ ls /tmp/bmv2-*
        ```

    3. You will **find ONOS netcfg JSON files in this folder** for each BMv2
        switch, open this file up, for example:

        ```
        $ cat /tmp/bmv2-s1-netcfg.json
        ```

        It contains the configuration for (1) the gRPC server and port used by the
        BMv2 switch process for the P4Runtime service, (2) the ID of pipeconf to
        deploy on the device, (3) switch ports details, and other
        driver-specific information.

        **This file is pushed to ONOS automatically by Mininet when executing
        the switch instance**. If everything went as expected, you should see
        the ONOS log populating with messages like:

        ```
        Connecting to device device:bmv2:s1 with driver bmv2
        [...]
        Setting pipeline config for device:bmv2:s1 to p4-tutorial-pipeconf...
        [...]
        Device device:bmv2:s1 connected
        [...]
        ```

    4. **Check the BMv2 switch instance log**:

        ```
        $ less /tmp/bmv2-s1-log
        ```

        By scrolling the BMv2 log, you should see all P4Runtime messages
        received by the switch. These messages are sent by ONOS and are used to
        install table entries and to read counters. You should also see many
        `PACKET_IN` and `PACKET_OUT` messages corresponding to packet-in/out
        processed by the switch and used for LLDP-based link discovery.

        Table entry messages are generated by ONOS according to the flow rules
        generated by each app and based on the P4Info associated with
        the `p4-tutorial-pipeconf`.

        If you prefer to watch the BMv2 log updating in real time, you can use
        the following command to print on screen all new messages:

        ```
        $ bm-log s1
        ```

        This command will show the log of the BMv2 switch in Mininet with name
        "s1".

        If needed, you can run BMv2 with **debug logging** enabled by passing
        the sub-argument `loglevel=debug` when starting Mininet. For example:

        ```
        $ sudo -E mn [...] --switch onosbmv2,loglevel=debug,pipeconf=p4-tutorial-pipeconf [...]
        ```

        Debug logging in BMv2 is useful to observe the life of a packet inside the
        pipeline, e.g. showing the header fields extracted by the parser for a
        specific packet, the tables used to process the packets, matching table
        entries (if any), etc.

    5. **Check the flow rules inserted by each app in ONOS**. In the
        ONOS CLI type:

        ```
        onos> flows -c
        ```

        You should see the following amount of flow rules on each device:

        ```
        deviceId=device:bmv2:s205, flowRuleCount=33
        deviceId=device:bmv2:s227, flowRuleCount=28
        deviceId=device:bmv2:s204, flowRuleCount=32
        deviceId=device:bmv2:s226, flowRuleCount=28
        ```
        You can also run the following command to view all of the flows.
        ```
        onos> flows -s
        ```

4. It is finally time to **test connectivity between the hosts** of our Mininet
    network.

    1. On the Mininet prompt, **start a ping between host1 and host2**:

        ```
        mininet> h1 ping h2
        ```

        The **ping should NOT work**, and the reason is that the host is not discovered by ONOS yet. 
        In a more complicated setup where DHCP relay is in use, ONOS can learn host information 
        when the host is requesting IP address using DHCP. 
        However, in this simple topology, ONOS only learns host information from ARP.

    2. To discover the hosts, we can **generate ARP packets** by the following command:

        ```
        mininet> h1 arping 10.0.2.254
        mininet> h2 arping 10.0.2.254
        mininet> h3 arping 10.0.3.254
        mininet> h4 arping 10.0.3.254
        ```

    3. Execute the following command to **verify all four hosts are discovered**:
        ```
        onos> hosts
        ```

        You should see 4 hosts.

    4. Start a ping between hosts. This time h1, h2 and h3 should be able to ping each other.
        ```
        mininet> h1 ping h2
        ```

        You should also notice that **host4 is not reachable**.
        The reason is that we have not configured the interface that host4 attaches to.

## Bonus exercise

5. Update network config to make host4 reachable
    1. Modify `trellisp4.json` and add the interface config on the port that host4 attaches to.

    2. You can copy the configuration of other ports.
    However, you may need to change device ID, port number, subnet or VLAN information accordingly.

    3. If you struggle to make it work, please ask the instructors for help. 
    Alternatively, you can find the solution in `trellisp4-full.json`.

## Congratulations, you completed the first lab of the Trellis+P4 tutorial!