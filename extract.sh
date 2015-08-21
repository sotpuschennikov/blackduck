#!/bin/bash -x
[[ -f centos61.csv ]] && [[ -f license_mos_6.1_rpm.csv ]] && python extract.py centos61.csv license_mos_6.1_rpm.csv rpm_output.csv || echo "Input files not found"
[[ -f ubuntu61.csv ]] && [[ -f license_mos_6.1_deb.csv ]] && python extract.py ubuntu61.csv license_mos_6.1_deb.csv deb_output.csv || echo "Input files not found"
