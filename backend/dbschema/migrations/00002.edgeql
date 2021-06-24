CREATE MIGRATION m1s4mvtpqrpc5utue7v5txfqp5egdv7oc32caf43wyzjn7p3mkvuka
    ONTO m1ben3hmdjvyluupqlmklfa6u3ouajw6tunh47563vvllmikoddg5q
{
  ALTER TYPE inventory::NetworkDevice {
      CREATE PROPERTY platform -> std::str;
  };
};
