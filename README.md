Fork of [node-sqlite3](https://github.com/mapbox/node-sqlite3), modified to use [SQLCipher](https://www.zetetic.net/sqlcipher/).

While the `node-sqlite3` project does include support for compiling against sqlcipher, it requires manual work, and does not work out-of-the-box on Electron on Windows. This fork changes the default configuration to bundle SQLCipher directly, as well as OpenSSL where required.

# Supported platforms

Windows, Mac and Linux.

# Requirements

### Windows

 * See [https://github.com/nodejs/node-gyp#on-windows](https://github.com/nodejs/node-gyp#on-windows)

### Mac

 * `brew install openssl`

# Installation

```sh
# Electron Example
npm i git+https://github.com/alex8088/node-sqlite3.git --build-from-source --runtime=electron --target_arch=ia32 --target=2.0.5 --dist-url=https://atom.io/download/electron
```

# Usage

``` js
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('test.db');

db.serialize(function() {
  db.run("PRAGMA key = 'mysecret'");
  db.run("CREATE TABLE lorem (info TEXT)");

  var stmt = db.prepare("INSERT INTO lorem VALUES (?)");
  for (var i = 0; i < 10; i++) {
      stmt.run("Ipsum " + i);
  }
  stmt.finalize();

  db.each("SELECT rowid AS id, info FROM lorem", function(err, row) {
      console.log(row.id + ": " + row.info);
  });
});

db.close();
```

# SQLCipher

A copy of the source for SQLCipher 4.2.0 is bundled, which is based on SQLite 3.28.0.

### OpenSSL

SQLCipher depends on OpenSSL. When using NodeJS, OpenSSL is provided by NodeJS itself. For Electron, we need to use our own copy.

For Windows we bundle OpenSSL 1.1.0. Pre-built libraries are used from https://slproweb.com/products/Win32OpenSSL.html.

On Mac we build against OpenSSL installed via brew, but statically link it so that end-users do not need to install it.

On Linux we dynamically link against the system OpenSSL.

# API

See the [API documentation](https://github.com/mapbox/node-sqlite3/wiki) in the wiki.

# Test

[mocha](https://github.com/visionmedia/mocha) is required to run unit tests.

In sqlite3's directory (where its `package.json` resides) run the following:

    npm install mocha
    npm test

# Powered By

- [node-sqlcipher](https://github.com/journeyapps/node-sqlcipher)

# License

[BSD licensed](./LICENSE).
