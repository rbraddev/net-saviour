module inventory{
    type NetworkDevice {
        required property nodeid -> int64 {
            constraint exclusive;
        };
        required property hostname -> str {
            constraint exclusive;
        };
        required property ip -> str {
            constraint exclusive;
        };
        property image -> str;
        required property active -> bool{
            default := true;
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
};