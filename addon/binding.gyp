{
  "variables": {
    'android_target%': '',
  },
  "targets": [
    {
      "target_name": "native-prover",
      "cflags!": ["-fno-exceptions"],
      "cflags_cc!": ["-fno-exceptions"],
      "cflags": ["-std=c++17", "-g", "-O3", "-pthread", "-fopenmp", "-Wno-unused-variable", "-Wno-gnu-designator", "-Wno-sign-compare" ],
      "cflags_cc": ["-std=c++17", "-g", "-O3", "-pthread", "-fopenmp", "-Wno-unused-variable", "-Wno-gnu-designator", "-Wno-sign-compare" ],
      "libraries": ["-pthread", "-lgmp", "-lsodium", "-fopenmp"],
      "defines": [
         "NAPI_CPP_EXCEPTIONS",
         "NAPI_VERSION=<(napi_build_version)"
      ],
      "sources": [
        "src/cpp/index.cpp",
        "src/cpp/prover.cpp",
        "src/cpp/rapidsnark/binfile_utils.cpp",
        "src/cpp/rapidsnark/zkey_utils.cpp",
        "src/cpp/ffiasm/misc.cpp",
        "src/cpp/ffiasm/naf.cpp",
        "src/cpp/ffiasm/splitparstr.cpp",
        "src/cpp/ffiasm/alt_bn128.cpp",
        "src/cpp/primefieldgmp/fq.cpp",
        "src/cpp/primefieldgmp/fr.cpp",
        "src/cpp/circuits/joinsplit_1x2/joinsplit_1x2_calcwit.cpp",
        "src/cpp/circuits/joinsplit_1x2/joinsplit_1x2_circuit.cpp",
        "src/cpp/circuits/joinsplit_1x2/joinsplit_1x2_createwit.cpp",
        "src/cpp/circuits/joinsplit_1x3/joinsplit_1x3_calcwit.cpp",
        "src/cpp/circuits/joinsplit_1x3/joinsplit_1x3_circuit.cpp",
        "src/cpp/circuits/joinsplit_1x3/joinsplit_1x3_createwit.cpp",
        "src/cpp/circuits/joinsplit_2x2/joinsplit_2x2_calcwit.cpp",
        "src/cpp/circuits/joinsplit_2x2/joinsplit_2x2_circuit.cpp",
        "src/cpp/circuits/joinsplit_2x2/joinsplit_2x2_createwit.cpp",
        "src/cpp/circuits/joinsplit_2x3/joinsplit_2x3_calcwit.cpp",
        "src/cpp/circuits/joinsplit_2x3/joinsplit_2x3_circuit.cpp",
        "src/cpp/circuits/joinsplit_2x3/joinsplit_2x3_createwit.cpp",
        "src/cpp/circuits/joinsplit_8x2/joinsplit_8x2_calcwit.cpp",
        "src/cpp/circuits/joinsplit_8x2/joinsplit_8x2_circuit.cpp",
        "src/cpp/circuits/joinsplit_8x2/joinsplit_8x2_createwit.cpp"
      ],
      "include_dirs": [
        "<!@(node -p \"require('node-addon-api').include_dir\")",
        "src/cpp",
        "src/cpp/dep",
        "src/cpp/dep/gmplib/include",
        "src/cpp/rapidsnark",
        "src/cpp/ffiasm",
        "src/cpp/primefieldgmp",
        "src/cpp/circuits",
        "src/cpp/circuits/joinsplit_1x2",
        "src/cpp/circuits/joinsplit_1x3",
        "src/cpp/circuits/joinsplit_2x2",
        "src/cpp/circuits/joinsplit_2x3",
        "src/cpp/circuits/joinsplit_8x2"
      ],
      "conditions": [
        ["OS=='mac'", {
          "xcode_settings": {
            "GCC_SYMBOLS_PRIVATE_EXTERN": "YES",
            "GCC_ENABLE_CPP_EXCEPTIONS": "YES",
            "MACOSX_DEPLOYMENT_TARGET": "12.3",

            "OTHER_CFLAGS": [ "-std=c++17", "-O3", "-Wno-unused-variable", "-Wno-sign-compare", "-Wno-gnu-designator", "-Xclang", "-fopenmp"],
            "cflags+": [ '-fvisibility=hidden', "-Xclang", "-fopenmp" ],
            "cflags!": ["-fno-exceptions"],
            "cflags_cc!": ["-fno-exceptions"]
          },
          "cflags_cc+": ["-Xclang", "-fopenmp" ],
          "libraries!": [ "-fopenmp" ],
          "libraries": [
            "-lomp -L<(module_root_dir)/src/cpp/dep/openmp/darwin-arm64/lib",
            "<!@(pkg-config libsodium --libs)",
            "<!@(pkg-config gmp --libs)",
          ],
          "include_dirs+": [
            "src/cpp/dep/openmp/darwin-arm64/include",
            "<!@(pkg-config libsodium --cflags-only-I | sed s/-I//g)",
            "<!@(pkg-config gmp --cflags-only-I | sed s/-I//g)",
          ],
        }],
        ["OS=='ios'", {
          "xcode_settings": {
            "GCC_SYMBOLS_PRIVATE_EXTERN": "YES",
            "GCC_ENABLE_CPP_EXCEPTIONS": "YES",
            "OTHER_CFLAGS": [ "-std=c++17", "-O3", "-Wno-unused-variable", "-Wno-sign-compare", "-Wno-gnu-designator", "-Xclang", "-fopenmp"],
            "IPHONEOS_DEPLOYMENT_TARGET": "9.0",
          },
          "include_dirs+": [
            "src/cpp/dep/openmp/ios/include/",
            "src/cpp/dep/libsodium/include"
          ],
          "libraries!": [ "-lgmp", "-fopenmp" ],
          "libraries": [
            "<(module_root_dir)/src/cpp/dep/openmp/ios/lib/libomp.a",
            "-L<(module_root_dir)/src/cpp/dep/libsodium/libsodium-ios/lib"
          ],
          "conditions": [
            ["target_arch=='x64'", {
              "libraries": [ "<(module_root_dir)/src/cpp/dep/gmplib/iphonesimulator/libgmp.a" ],
            }],
            ["target_arch=='arm64'", {
              "libraries": [ "<(module_root_dir)/src/cpp/dep/gmplib/ios/libgmp.a" ],
            }],
          ]
        }],
        ["OS=='android'", {
          "cflags+": [ "-fPIC", "-static-openmp" ],
          "cflags_cc+": [ "-fPIC", "-static-openmp" ],
          "ldflags": [ "-fPIC", "-Wl,-z,notext", "-static-openmp" ],
          "cflags!": [
            "-fno-tree-vrp",
            "-mfloat-abi=hard",
            "-fPIE"
          ],
          "ldflags!": [ "-fPIE" ],
          "include_dirs+": [
            "src/cpp/dep/libsodium/include"
          ],
          "libraries!": [ "-lgmp", "-lsodium" ],
          "libraries": [
            "<(module_root_dir)/src/cpp/dep/libsodium/android/<(android_target)/lib/libsodium.a",
            "<(module_root_dir)/src/cpp/dep/gmplib/android/<(android_target)/libgmp.a",
          ]
        }],
      ]
    }
  ]
}
