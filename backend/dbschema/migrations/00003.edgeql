CREATE MIGRATION m1abpelddoyanai7ov7aiu2nsylqszght7v5o4jat6bav2vhy6kkqa
    ONTO m1yxvaodwlqhdlbkkquttu4xfa32zld2d3oernttzzi7khda6afzhq
{
  ALTER TYPE inventory::Desktop {
      ALTER PROPERTY cidr {
          SET TYPE std::int64;
      };
      ALTER PROPERTY nodeid {
          SET TYPE std::int64;
      };
  };
  ALTER TYPE inventory::Interface {
      ALTER PROPERTY cidr {
          SET TYPE std::int64;
      };
      ALTER PROPERTY vlan {
          SET TYPE std::int64;
      };
  };
  ALTER TYPE inventory::NetworkDevice {
      ALTER PROPERTY nodeid {
          SET TYPE std::int64;
      };
  };
};
