{
  'includes': [ 'common-sqlite.gypi' ],
  'target_defaults': {
    'default_configuration': 'Release',
    'cflags':[
      '-std=c99'
    ],
    'configurations': {
      'Debug': {
        'defines': [ 'DEBUG', '_DEBUG' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'RuntimeLibrary': 1, # static debug
          },
        },
      },
      'Release': {
        'defines': [ 'NDEBUG' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'RuntimeLibrary': 0, # static release
          },
        },
      }
    },
    'msvs_settings': {
      'VCCLCompilerTool': {
      },
      'VCLibrarianTool': {
      },
      'VCLinkerTool': {
        'GenerateDebugInformation': 'true',
      },
    },
    'conditions': [
      ['OS == "win"', {
        'defines': [
          'WIN32'
        ],
        'conditions':[      # set libraries path for windows target_arch
          ['target_arch == "ia32"',{
            'variables': {
              'LIB_root%': 'LIB-Win32',
            }
          }],
          ['target_arch == "x64"',{
            'variables': {
              'LIB_root%': 'LIB-Win64',
            }
          }]
        ],
        'link_settings': {
          'library_dirs': [
            '<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/<(LIB_root)'
          ],
          'libraries': [
            '-lCrypt32.Lib',      # Link Windows library setting (electron build requirements)
            '-lWS2_32.Lib',       # Link Windows library setting (electron build requirements)
            '-llibcrypto.lib',    # Customized openssl static library (remove /Zi disable debug)
            '-llibssl.lib'        # Customized openssl static library (remove /Zi disable debug)
          ]
        }
      }],
      ['OS == "mac"', {
        'variables': {
          'LIB_root%': '/usr/local/opt/openssl'
        },
        'link_settings': {
          'libraries': [
            # This statically links libcrypto, whereas -lcrypto would dynamically link it
            '<(LIB_root)/lib/libcrypto.a'
          ]
        }
      }],
      ['OS == "linux"', {
        'link_settings': {
          'libraries': [
            '-lcrypto'
          ]
        }
      }]
    ]
  },

  'targets': [
    {
      'target_name': 'action_before_build',
      'type': 'none',
      'hard_dependency': 1,
      'actions': [
        {
          'action_name': 'unpack_sqlite_dep',
          'inputs': [
            './sqlcipher-amalgamation-<@(sqlite_version).tar.gz'
          ],
          'outputs': [
            '<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/sqlite3.c'
          ],
          'action': ['<!(node -p "process.env.npm_config_python || \\"python\\"")','./extract.py','./sqlcipher-amalgamation-<@(sqlite_version).tar.gz','<(SHARED_INTERMEDIATE_DIR)']
        }
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/',
        ]
      },
    },
    {
      'target_name': 'sqlite3',
      'type': 'static_library',
      "conditions": [
        ['OS == "win"', {
          'include_dirs': [
            '<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/',
            '<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/include'
          ],
          'conditions':[        # Openssl opensslconf.h on Windows ia32 is different than x64.
            ['target_arch == "ia32"',{
              "copies": [{
                "files": ["<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/include/win32/opensslconf.h"],
                "destination": "<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/include/openssl"
              }]
            }],
            ['target_arch == "x64"',{
              "copies": [{
                "files": ["<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/include/win64/opensslconf.h"],
                "destination": "<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/include/openssl"
              }]
            }]
          ]
        }],
        ['OS == "mac"', {
          'include_dirs': [
            '<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/',
            '>(LIB_root)/include'
          ]
        }],
        ['OS == "linux"', {
          'include_dirs': [
            '<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/'
          ]
        }]
      ],
      'dependencies': [
        'action_before_build'
      ],
      'sources': [
        '<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/sqlite3.c'
      ],
      'direct_dependent_settings': {
        'include_dirs': [ '<(SHARED_INTERMEDIATE_DIR)/sqlcipher-amalgamation-<@(sqlite_version)/' ],
        'defines': [
          'SQLITE_THREADSAFE=1',
          'HAVE_USLEEP=1',
          'SQLITE_ENABLE_FTS3',
          'SQLITE_ENABLE_FTS4',
          'SQLITE_ENABLE_FTS5',
          'SQLITE_ENABLE_JSON1',
          'SQLITE_ENABLE_RTREE',
          'SQLITE_HAS_CODEC',
          'SQLITE_TEMP_STORE=2',
          'SQLITE_SECURE_DELETE'
        ],
      },
      'cflags_cc': [
          '-Wno-unused-value'
      ],
      'defines': [
        '_REENTRANT=1',
        'SQLITE_THREADSAFE=1',
        'HAVE_USLEEP=1',
        'SQLITE_ENABLE_FTS3',
        'SQLITE_ENABLE_FTS4',
        'SQLITE_ENABLE_FTS5',
        'SQLITE_ENABLE_JSON1',
        'SQLITE_ENABLE_RTREE',
        'SQLITE_HAS_CODEC',
        'SQLITE_TEMP_STORE=2',
        'SQLITE_SECURE_DELETE'
      ],
      'export_dependent_settings': [
        'action_before_build',
      ]
    }
  ]
}
