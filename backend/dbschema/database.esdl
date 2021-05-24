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
        property site -> str;
        required property active -> bool{
            default := true;
        };
        index on (__subject__.nodeid);
        index on (__subject__.ip);
    };
    type Desktop {
        required property hostname -> str {
            constraint exclusive;
        };
        required property ip -> str {
            constraint exclusive;
        };
        required property mac -> str {
            constraint exclusive;
        };
        link switch -> NetworkDevice;
        property switch_port -> str;
        index on (__subject__.hostname);
        index on (__subject__.ip);
        index on (__subject__.mac);
    };
};