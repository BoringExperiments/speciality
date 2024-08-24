The [Play Integrity API](https://developer.android.com/google/play/integrity) is a feature that replaces the now deprecated [SafetyNet Attestation API](https://developer.android.com/privacy-and-security/safetynet/attestation) to detect potentially modified or infected (or Play Protect-disabled) Android devices.

## Motivation

Regular user **should not** install applications outside of their provided app stores or unlock their bootloader, root or install customised Android OS without proper incentive or knowledge of the Android OS as a whole as this only opens up additional attack surface. 

Many banking applications implemented extreme measures to prevent unauthorised access[^1], modification and root with methods such as outright blocking certain applications from using the accessibility service, VPN-sensing, anti-hooking and/or 3rd-party solutions (e.g., [Guardsquare](https://www.guardsquare.com/), [AppSealing](https://www.appsealing.com/android-app-security/)) to prevent (i.e., dangerous application with accessibility-enabled or Magisk/KernelSU module) from taking over the application.

By using Play Integrity API we can check the OS and (does not apply) application integrity simultaneously without implementing too many features.

## Consideration

> [!IMPORTANT]
> 
> * 💥 Using the Play Integrity API on below Android 11 **may** report as `MEETS_DEVICE_INTEGRITY` instead of the highest `MEETS_STRONG_INTEGRITY` label. <br>
>   I'm not sure why Android 11 specifically but according to the [Android CDD](https://source.android.com/docs/compatibility/12/android-12-cdd), Android 12 has upped their security a lot and might be the sweet spot to getting the highest integrity label on every device.

* Locally attested Play Integrity API may not be as secure as Google-attested Play Integrity API.
  * (not sure) Devices with privacy-centric (e.g., Graphene OS) ROMs **may** not be able to use this unless they install Play Services.
* The API will not be able to verify the integrity of the application unless the app is published to the Google Play Store.

[^1]: Most banking applications in Thailand such as SCB Mobile, KBank, Bangkok Bank, etc. have implemented one or more following features to prevent unauthorised access.
