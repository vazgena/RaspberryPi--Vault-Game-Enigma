CREATE TABLE trackers_raw(moment TIMESTAMP(6), rssi SMALLINT, tx_power SMALLINT, beacon_mac VARCHAR(100), room VARCHAR(20), station VARCHAR(20) ) ;
CREATE INDEX trackers_raw_moment ON trackers_raw(moment);

