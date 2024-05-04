# **Determin HA States for F5, ISE, and Palo Alto Panorama**

## → **Summary**
| **Module** | **Import Path** | **Description** |
|---|---|---|
| **F5** | **hastate.f5** | Functions to interact with F5 LTMs and GTMs. |
| **ISE** | **hastate.ise** | Functions to determine ISE primary node for PAN devices, and determine number of active users on MNT. |
| **Palo Alto** | **hastate.paloalto** | Functions to interact with the Palo Alto Panorama API.|

## → **Installation**
Install using pip:

```bash
$ cd haState
$ pip install .
```
## → **Usage Examle F5**
```python
from hastate.f5 import f5_ha_state
# Determine between pairs
ltmPair = ['ltm1', 'ltm2']
active = f5_ha_state(username, password, ltmPair)

# Determine state of 1 device
ltm = ['ltm1']
active, standby = f5_ha_state(username, password, ltm)
```

## → **Usage Examle ISE**
```python
from hastate.ise import ise_ha_state, ise_active_dc
# Determine between pairs.
isePair = ['isePan1', 'isePan2']
active = ise_ha_state(sername, password, isePair)

# Determine state of 1 device.  If secondary device will return None, None.
ise = ['ltm1']
active, standby = f5_ha_state(username, password, ise)
```
## → **Usage Examle Palo Alto Panorama**
```python
from hastate.paloalto import pan_ha_state
# Determine state of pairs.
panPair = ['pan1', 'pan2']
active = pan_ha_state(username, password, panPair)

# Use default settings
active = pan_ha_state(username, password)
```