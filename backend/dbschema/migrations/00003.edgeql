CREATE MIGRATION m1jm5dthh76b2jzjihpx4b6e5slnluwuo4fyxtobthwp33vfsl6vpa
    ONTO m1s4mvtpqrpc5utue7v5txfqp5egdv7oc32caf43wyzjn7p3mkvuka
{
  ALTER TYPE inventory::NetworkDevice {
      CREATE PROPERTY device_type -> std::str;
  };
};
