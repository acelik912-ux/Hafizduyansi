plugins {
    id("com.android.application")
    id("kotlin-android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.hafizdunyasi.hafiz_dunyasi"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_17.toString()
    }

    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "com.hafizdunyasi.gezgin"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    // Sabit imza anahtarı: her bilgisayarda ve GitHub Actions'ta aynı anahtarla imzalanır,
    // böylece yeni APK telefondaki eskisinin ÜSTÜNE kurulur (kayıtlar silinmez).
    // Anahtarı ASLA değiştirme; değişirse üstüne kurulum bozulur.
    val anahtar = file("../hafiz-release.keystore")
    signingConfigs {
        create("hafiz") {
            if (anahtar.exists()) {
                storeFile = anahtar
                storePassword = "hafizdunyasi2026"
                keyAlias = "hafiz"
                keyPassword = "hafizdunyasi2026"
            }
        }
    }

    buildTypes {
        release {
            signingConfig = if (anahtar.exists()) signingConfigs.getByName("hafiz") else signingConfigs.getByName("debug")
        }
    }
}

flutter {
    source = "../.."
}
