module inventory{
    type NetworkDevice {
        required property hostname -> str {
            constraint exclusive;
        };
        required property ip -> str {
            constraint exclusive;
        };
    };
    type Desktop {
        required property hostname -> str {
            constraint exclusive;
        };
        required property ip -> str {
            constraint exclusive;
        };
        link switch -> NetworkDevice;
        property switch_port -> str;
    };
    type User {
        required property username -> str;
        property is_superuser -> bool {
            default := false;
        };
        property is_active -> bool {
            default := false;
        };
    };
};