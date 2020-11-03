# NET-Saviour

A network configuration and trouble shooting tool

Required environment variables:

* AUTH_MODE - This defines the authenticate mode used.

    Current options:

    *   tacacs

            when using TACACS you mush provide the following environment variables:

            * TACACS_HOST - This is the TACACS server ip or hostname. It defaults to localhost
            * TACACS_KEY - This is the TACACS secret
