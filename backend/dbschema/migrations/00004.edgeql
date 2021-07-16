CREATE MIGRATION m1ggpoxnim5q7uyfxpdbc5iupkiqe4dx3ytuxfz7wowqw3gy5cjnda
    ONTO m1abpelddoyanai7ov7aiu2nsylqszght7v5o4jat6bav2vhy6kkqa
{
  ALTER TYPE inventory::Desktop {
      ALTER PROPERTY cidr {
          SET TYPE std::int16;
      };
      ALTER PROPERTY nodeid {
          SET TYPE std::int16;
      };
  };
  ALTER TYPE inventory::Interface {
      ALTER PROPERTY cidr {
          SET TYPE std::int16;
      };
      ALTER PROPERTY vlan {
          SET TYPE std::int16;
      };
  };
  ALTER TYPE inventory::NetworkDevice {
      ALTER PROPERTY nodeid {
          SET TYPE std::int16;
      };
  };
};
