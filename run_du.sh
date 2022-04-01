#!/bin/bash

DU_MODE=${CONFIG_DU_MODE:=INTEL}

[ "$DU_MODE" = "PAL" ] && DU_PATH=du_bin_pal || DU_PATH=du_bin_intel

echo -ne "\033]0;GNB-DU ($DU_MODE)\007"

SYNERGY_DIR=/home/pegauser/synergy

CU_BIN_ROOT_PATH=${SYNERGY_DIR}/cu_bin
DU_BIN_ROOT_PATH=${SYNERGY_DIR}/${DU_PATH}
CONFIG_DIR=${SYNERGY_DIR}/config
OAM_DIR=${SYNERGY_DIR}/oam_sysrepo
#OAM_DIR=${DU_BIN_ROOT_PATH}/liboam/oam_du/cm
TEMPLATE_DIR=${CONFIG_DIR}/du_template

OAM_TEMPLATE=$TEMPLATE_DIR/oam_template_du.xml
OAM_CONFIG=$CONFIG_DIR/oam_sysrepo_du.xml
OAM_CONFIG_MODE=$CONFIG_DU_OAM_CONFIG_MODE

[ "$DU_MODE" = "PAL" ] && SYS_CONFIG_PATH=$CONFIG_DIR/du_config_pal || SYS_CONFIG_PATH=$CONFIG_DIR/du_config

SYS_CONFIG=$SYS_CONFIG_PATH/sys_config.txt
SYS_CONFIG_MODE=$CONFIG_DU_SYS_CONFIG_MODE

###_PEGA RU_: 1:VIAVI_FREQ_3500580, 2:Keysight_FREQ_3500580, 3:WNC, 4:FOXCONN, 5:VIAVI_FREQ_3746820, 6:WNC_n79_4849860###
RU_ID=3

DU_F1C_IF=
DU_F1C_IP4=
DU_F1C_IP4_PLEN=
DU_F1U_IF=
DU_F1U_IP4=
DU_F1U_IP4_PLEN=

get_ip4_addr() {
        local ip4=$(ip -o -4 addr list $1 | awk '{print $4}' | cut -d/ -f1)
        echo $ip4
}

get_ip4_plen() {
        local plen=$(ip -o -4 addr list $1 | awk '{print $4}' | cut -d/ -f2)
        echo $plen
}

get_ip6_addr() {
        local ip6=$(ip -o -6 addr list $1 | awk '{print $4}' | cut -d/ -f1)
        echo $ip6
}

get_ip6_plen() {
        local plen=$(ip -o -6 addr list $1 | awk '{print $4}' | cut -d/ -f2)
        echo $plen
}

load_network_config() {
        CONFIG_GNBID=${CONFIG_GNBID:-1}
        CONFIG_NRPCI=${CONFIG_NRPCI:-1}
        CONFIG_GNBDUID=${CONFIG_GNBDUID:-1}
        CONFIG_NRCELLID=${CONFIG_NRCELLID:-000000001}
        CONFIG_ULP0NOMINAL=${CONFIG_ULP0NOMINAL:--70}
        CONFIG_PRERCVDTGTPWR=${CONFIG_PRERCVDTGTPWR:--74}
        CONFIG_PRETRANSMAX=${CONFIG_PRETRANSMAX:-preambleTransMax_n10}
        CONFIG_MAXMSG3TX=${CONFIG_MAXMSG3TX:-0}
        CONFIG_PUSCHP0NOMINAL=${CONFIG_PUSCHP0NOMINAL:--74}
        CONFIG_PUCCHP0NOMINAL=${CONFIG_PUCCHP0NOMINAL:--74}
        CONFIG_NSSBPWR=${CONFIG_NSSBPWR:--10}
        CONFIG_TACBITMAP=${CONFIG_TACBITMAP:-1}
        CONFIG_NRTAC=${CONFIG_NRTAC:-0001}

        echo "======================================="
        echo "Network Configuration:"
        echo "  CONFIG_5GC_MCC=$CONFIG_5GC_MCC"
        echo "  CONFIG_5GC_MNC=$CONFIG_5GC_MNC"

        echo "  CONFIG_DU_NET_F1C=$CONFIG_DU_NET_F1C"
        echo "  CONFIG_DU_PCI_F1C=$CONFIG_DU_PCI_F1C"
        echo "  CONFIG_DU_IF_F1C=$CONFIG_DU_IF_F1C"

        echo "  CONFIG_DU_NET_F1U=$CONFIG_DU_NET_F1U"
        echo "  CONFIG_DU_PCI_F1U=$CONFIG_DU_PCI_F1U"
        echo "  CONFIG_DU_IF_F1U=$CONFIG_DU_IF_F1U"

        echo "  CONFIG_GNBID=${CONFIG_GNBID}"
        echo "  CONFIG_NRPCI=${CONFIG_NRPCI}"
        echo "  CONFIG_GNBDUID=${CONFIG_GNBDUID}"
        echo "  CONFIG_NRCELLID=${CONFIG_NRCELLID}"

        RU_ID=${CONFIG_RU_ID:-3}

        ###_PEGA RU_: 1:VIAVI, 2:Keysight, 3:WNC, 4:FOXCONN, 5:VIAVI_FREQ_3746820, 6.WNC_n79_4849860 ###
        case $RU_ID in
        1)
                RU_TYPE=viavi
        ;;
        2)
                RU_TYPE=keysight
        ;;
        3)
                RU_TYPE=wnc
        ;;
        4)
                RU_TYPE=foxconn
        ;;
        5)
                RU_TYPE=viaviori
        ;;
        6)
                RU_TYPE=wnc_n79
        ;;
        esac
        echo "======================================="
        echo "RU Configuration:"
        echo "  CONFIG_RU_ID=$CONFIG_RU_ID"
        echo "  CONFIG_ULP0NOMINAL=${CONFIG_ULP0NOMINAL}"
        echo "  CONFIG_PRERCVDTGTPWR=${CONFIG_PRERCVDTGTPWR}"
        echo "  CONFIG_PRETRANSMAX=${CONFIG_PRETRANSMAX}"
        echo "  CONFIG_MAXMSG3TX=${CONFIG_MAXMSG3TX}"
        echo "  CONFIG_PUSCHP0NOMINAL=${CONFIG_PUSCHP0NOMINAL}"
        echo "  CONFIG_PUCCHP0NOMINAL=${CONFIG_PUCCHP0NOMINAL}"
        echo "  CONFIG_NSSBPWR=${CONFIG_NSSBPWR}"

        DU_F1C_IF=${CONFIG_DU_IF_F1C:-du-f1c}
        DU_F1U_IF=${CONFIG_DU_IF_F1U:-du-f1u}

        DU_F1C_IP4=$(get_ip4_addr $DU_F1C_IF)
        DU_F1C_IP4_PLEN=$(get_ip4_plen $DU_F1C_IF)

        DU_F1U_IP4=$(get_ip4_addr $DU_F1U_IF)
        DU_F1U_IP4_PLEN=$(get_ip4_plen $DU_F1U_IF)

                [ -z "$CONFIG_CU_NET_F1C" ] && {
                        echo "Failed to get CONFIG_CU_NET_F1C for DU. "
                        return 1
                }

                [ -z "$CONFIG_CU_NET_F1U" ] && {
                        echo "Failed to get CONFIG_CU_NET_F1U for DU. "
                        return 1
                }

        CU_F1C_IF="cu-f1c"
                CU_F1C_IP4=$(echo $CONFIG_CU_NET_F1C | cut -d/ -f1)
                CU_F1C_IP4_PLEN=$(echo $CONFIG_CU_NET_F1C | cut -d/-f2)

                CU_F1U_IF="cu-f1u"
                CU_F1U_IP4=$(echo $CONFIG_CU_NET_F1U | cut -d/ -f1)
                CU_F1U_IP4_PLEN=$(echo $CONFIG_CU_NET_F1U | cut -d/ -f2)

        echo "======================================="
        echo "Network Status:"
        echo "  CU$CONFIG_GNBID   F1C($CU_F1C_IF) IPv4 Addr : $CU_F1C_IP4/$CU_F1C_IP4_PLEN"
        echo "  CU$CONFIG_GNBID   F1U($CU_F1U_IF) IPv4 Addr : $CU_F1U_IP4/$CU_F1U_IP4_PLEN"
        echo "  DU$CONFIG_GNBDUID F1C($DU_F1C_IF) IPv4 Addr : $DU_F1C_IP4/$DU_F1C_IP4_PLEN"
        echo "  DU$CONFIG_GNBDUID F1U($DU_F1U_IF) IPv4 Addr : $DU_F1U_IP4/$DU_F1U_IP4_PLEN"
        echo "======================================="

}



generate_oam_config() {
        local config=$1
        local template=$2

echo "s/##MCC##/$CONFIG_5GC_MCC/" > /tmp/oam.sc
echo "s/##MNC##/$CONFIG_5GC_MNC/" >> /tmp/oam.sc
echo "s/##gNBId##/$CONFIG_GNBID/" >> /tmp/oam.sc
echo "s/##f1cPeerIpAddr##/$CU_F1C_IP4/" >> /tmp/oam.sc
echo "s/##f1uPeerIpAddr##/$CU_F1U_IP4/" >> /tmp/oam.sc
echo "s/##f1cIpAddr##/$DU_F1C_IP4/" >> /tmp/oam.sc
echo "s/##f1uIpAddr##/$DU_F1U_IP4/" >> /tmp/oam.sc
echo "s/##gNBId##/$CONFIG_GNBID/" >> /tmp/oam.sc
echo "s/##gNBDUId##/$CONFIG_GNBDUID/" >> /tmp/oam.sc
echo "s/##nrCellId##/$CONFIG_NRCELLID/" >> /tmp/oam.sc
echo "s/##nRPCI##/$CONFIG_NRPCI/" >> /tmp/oam.sc

echo "s/##ulp0nominal##/$CONFIG_ULP0NOMINAL/" >> /tmp/oam.sc
echo "s/##preambleRcvdTgtPwr##/$CONFIG_PRERCVDTGTPWR/" >> /tmp/oam.sc
echo "s/##preambleTransMax##/$CONFIG_PRETRANSMAX/" >> /tmp/oam.sc
echo "s/##maxMsg3Tx##/$CONFIG_MAXMSG3TX/" >> /tmp/oam.sc
echo "s/##puschp0nominal##/$CONFIG_PUSCHP0NOMINAL/" >> /tmp/oam.sc
echo "s/##pucchp0nominal##/$CONFIG_PUCCHP0NOMINAL/" >> /tmp/oam.sc
echo "s/##nSsbPwr##/$CONFIG_NSSBPWR/" >> /tmp/oam.sc
echo "s/##tacbitmap##/$CONFIG_TACBITMAP/" >> /tmp/oam.sc
echo "s/##nrtac##/$CONFIG_NRTAC/" >> /tmp/oam.sc

        sed -f /tmp/oam.sc $template > $config

}


load_oam_config() {
        python3 /home/pegauser/synergy/change_oam_sysrepo_du_params.py
        local ret=0
        local install=1

        [ ! -d /tmp/config ] && mkdir -p /tmp/config

        case $OAM_CONFIG_MODE in
        k8s)
                OAM_CONFIG=/tmp/config/config.xml
        ;;
        netconf)
                OAM_CONFIG=/tmp/config/config.xml
                install=0
        ;;
        esac

        [ $install -eq 1 ] && {
                echo "Install OAM(sysrepo) Schema ..."
                cd $OAM_DIR/yang_r2.1 && sudo ./install_schema.sh
        }

        config=$OAM_CONFIG

        # find template file
        template=$OAM_TEMPLATE
        [ ! -f $template ] && {
                template=$TEMPLATE_DIR/oam_template_du_${RU_TYPE}.xml

                sudo cp $template $OAM_TEMPLATE
        }


        [ ! -f $config ] && {
                echo "Not found imported OAM configuration, generating by ENV. "
                generate_oam_config $config $OAM_TEMPLATE
        }

        echo "Import OAM(sysrepo) configuration $config ($OAM_CONFIG_MODE)... "

        [ ! -f $config ] && {
                echo "Failed to find valid OAM configuration. "
                return 1
        }

        # import to "startup" Datastore [persistent]
        sudo sysrepocfg -d "startup" --edit=$config
        sudo sysrepocfg -C "startup"

        #case $SYS_CONFIG_MODE in
        #        k8s-manual)
        #                echo "NETCONF/CONFD port assign ..."
        #                OAM_DU_CONFD_PORT=${CONFIG_DU_OAM_CONFD_PORT:-11000}
        #                OAM_DU_NETCONF_PORT=${CONFIG_DU_OAM_NETCONF_PORT:-2100}
        #               echo "OAM_DU_CONFD_PORT=$OAM_DU_CONFD_PORT"
        #               echo "OAM_DU_NETCONF_PORT=$OAM_DU_NETCONF_PORT"
        #                sed -i "s/1100*/$OAM_DU_CONFD_PORT/g" /home/pegauser/synergy/du_bin_intel/config/oam_du_confd_cfg.txt
        #                sed -i "s/1100*/$OAM_DU_CONFD_PORT/g" /home/pegauser/synergy/du_bin_intel/liboam/oam_du/cm/confd/config/confd.conf
        #                sed -i "s/210*/$OAM_DU_NETCONF_PORT/g" /home/pegauser/synergy/du_bin_intel/liboam/oam_du/cm/confd/config/confd.conf
        #       ;;
        #esac
        #local confd_pid=$(pgrep confd)
        #[ ! -n "$confd_pid" ] && {
        #       echo "Starting ConfD ..."
        #       source /opt/confd-basic-7.5.2/confdrc && \
        #       cd /home/pegauser/synergy/du_bin_intel/liboam/oam_du/cm/confd/run/ && \
        #       confd -c ../config/confd.conf --addloadpath /opt/confd-basic-7.5.2/etc/confd/
        #}

        #case $SYS_CONFIG_MODE in
        #        k8s-manual)
        #               CONFD_IPC_PORT=$OAM_DU_CONFD_PORT confd_load -l $config
        #       ;;
        #       *)
        #               CONFD_IPC_PORT=11000 confd_load -l $config
        #       ;;
        #esac
        ret=$?

        return $ret
}


update_sys_config() {
        CPU_LIST_AUTO=$(taskset -cp $$ | grep -oE '[0-9,-]+$')
        F1C_PCI_ADDR_AUTO=$PCIDEVICE_INTEL_COM_PCI_SRIOV_NET_F1C
        F1U_PCI_ADDR_AUTO=$PCIDEVICE_INTEL_COM_PCI_SRIOV_NET_F1U
        CPU_TABLE_INDEX=$CONFIG_DU_CPUTABLEIDX


        echo "======================================="
        echo "Allocated Resources:"
        echo "  CPU List        : $CPU_LIST_AUTO"
        echo "  F1C PCI Addr    : $F1C_PCI_ADDR_AUTO"
        echo "  F1U PCI Addr    : $F1U_PCI_ADDR_AUTO"
        echo "======================================="
        CPU_LIST=$CPU_LIST_AUTO
        CPU_TABLE=$CPU_TABLE_INDEX

        case $SYS_CONFIG_MODE in
                k8s-manual)
                        echo "SYSCONFIG mode: Manual"

                        cp -f /tmp/sysconfig/* $SYS_CONFIG_PATH/

                        [ -n "$CONFIG_DU_CPU_LIST" ] && CPU_LIST=$CONFIG_DU_CPU_LIST

                        echo "  CPU Pinning mode : $CPU_LIST"

                        # Update CPU list
                        cd $SYNERGY_DIR
                        python3 $SYNERGY_DIR/config_parser.py $SYS_CONFIG ${CPU_LIST} du ${CPU_TABLE}
                        WLS_COREMASK=`cat /tmp/WLS_COREMASK.txt`
                ;;

                k8s)
                        echo "SYSCONFIG mode: Auto"

                        echo "  CPU Pinning mode: ${CPU_LIST}"

                        # Update CPU list
                        cd $SYNERGY_DIR
                        python3 $SYNERGY_DIR/config_parser.py $SYS_CONFIG ${CPU_LIST} du ${CPU_TABLE}
                        WLS_COREMASK=`cat /tmp/WLS_COREMASK.txt`
                ;;

                *)
                        echo "SYSCONFIG mode: configMap"

                        cp -f /tmp/sysconfig/* $SYS_CONFIG_PATH/
                        echo "CPU Pinning mode: configMap"
                ;;
        esac

        echo "======================================="
}


load_sys_config() {

        DU_SYS_CONFIG=$SYS_CONFIG_PATH

        echo "Import system configuration $config ($CONFIG_DU_SYS_CONFIG_MODE)... "
        cp -f $DU_SYS_CONFIG/* $DU_BIN_ROOT_PATH/config/
}

start_du() {
        cd $DU_BIN_ROOT_PATH/bin
        export LD_LIBRARY_PATH=.:/usr/local/lib:/usr/local/lib64/:.
        echo "Starting DU..."
        echo "  DPDK_DEV        : $DPDK_DEV"
        echo "  WLS_DEV         : $WLS_DEV"
        echo "  WLS_COREMASK    : $WLS_COREMASK"

        sudo env LD_LIBRARY_PATH=$LD_LIBRARY_PATH HUGE_DIR=$HUGE_DIR WLS_DEV=$WLS_DEV WLS_MEMORY_SIZE=$WLS_MEMORY_SIZE WLS_COREMASK=$WLS_COREMASK DPDK_DEV=$DPDK_DEV ./gnb_du
}

stop_du() {
        echo "Stopping DU..."
        kill -9 `ps aux | grep gnb_du | awk '{print $2}'` > /dev/null
}

start() {

        [ "$DU_MODE" = "INTEL" ] && {
                while [  "`sudo cat /var/run/dpdk/$WLS_DEV/_health 2>/dev/null`" != "1" ];
                do
                        echo waiting for L1 ready
                        sleep 5
                done
        }

        start_du
}

load_network_config

load_oam_config

update_sys_config

load_sys_config

start

