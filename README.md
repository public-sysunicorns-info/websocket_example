# websocket_example

## Device Authentication Materials
Recommendation :
- Certificate ( Mutual TLS Authentication, one by Device ) using Hashicorp Vault and PKI Secret Engine ( DeviceId as CommonName )
- Client Id / Client Secret ( Client Credentials Flow, one by Device) using KeyCloak as Authentication / Authorization Server

But for Demo, it will use an API_KEY by Device

## Architecture Part
- Authentication / Authorization Server [ KeyCloak ] [ Status: TODO ]
- PKI [ HashicorpVault ] [ Status: TODO ]
- Device Communication Server [ Python FASTAPI ] [Status: InProgress]
- Cache Server [ Redis ]