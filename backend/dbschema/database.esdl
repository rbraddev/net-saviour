module inventory{
    abstract type Device{
            required property hostname -> str {
            constraint exclusive;
        };
        required property ip -> util::IP {
            constraint exclusive;
        };
        property site -> str;
        required property active -> bool{
            default := true;
        };
        index on (__subject__.ip);
        index on (__subject__.hostname);
    }

    type NetworkDevice extending Device{
        required property nodeid -> int16 {
            constraint exclusive;
        };
        property device_type -> str;
        property platform -> str;
        property model -> str;
        property image -> str;
        multi link interfaces -> Interface {
            on target delete allow;
        };
        index on (__subject__.nodeid);
    }

    type Desktop extending Device{
        required property nodeid -> int16 {
            constraint exclusive;
        };
        required property mac -> str {
            constraint exclusive;
        };
        property cidr -> int16;
        index on (__subject__.mac);
    }

    type Interface {
        required property mac -> str {
            constraint exclusive;
        };
        required property name -> str;
        property description -> str;
        property vlan -> int16;
        property ip -> util::IP;
        property cidr -> int16;
        link desktop -> Desktop;
        index on (__subject__.mac);
        index on (__subject__.ip);
    }
};