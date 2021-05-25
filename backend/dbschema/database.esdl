module inventory{
    abstract type Device{
        required property hostname -> str {
            constraint exclusive;
        };
        required property ip -> util::IP {
            constraint exclusive;
        };
        property site -> str;
        index on (__subject__.ip);
        index on (__subject__.hostname);
    }

    type NetworkDevice extending Device{
        required property nodeid -> int64 {
            constraint exclusive;
        };
        property model -> str;
        property image -> str;
        required property active -> bool{
            default := true;
        };
        multi link interfaces -> Interface;
        index on (__subject__.nodeid);
    }

    type Desktop extending Device{
        required property mac -> str {
            constraint exclusive;
        };
        index on (__subject__.mac);
    }

    type Interface {
        required property mac -> str {
            constraint exclusive;
        };
        required property name -> str;
        property description -> str;
        property ip -> util::IP;
        property subnet -> int16;
        link desktop -> Desktop;
        index on (__subject__.mac);
    }
};