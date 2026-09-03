1. 1 Шард 2 реплики (из выполнения предыдущего домашнего задания)
<clickhouse>
    <remote_servers>
      <cluster_1S_2R>
            <shard>
                <internal_replication>true</internal_replication>
                <replica>
                    <host>clickhouse-01</host>
                    <port>9000</port>
                    <user>chcluster</user>
                    <password>chcluster</password>
                </replica>
                <replica>
                    <host>clickhouse-02</host>
                    <port>9000</port>
                    <user>chcluster</user>
                    <password>chcluster</password>
                </replica>
            </shard>
        </cluster_1S_2R>
        <cluster_2S_1R>
            <shard>
                <replica>
                    <host>clickhouse-01</host>
                    <port>9000</port>
                    <user>chcluster</user>
                    <password>chcluster</password>
                </replica>
            </shard>
            <shard>
                <replica>
                    <host>clickhouse-02</host>
                    <port>9000</port>
                    <user>chcluster</user>
                    <password>chcluster</password>
                </replica>
            </shard>
        </cluster_2S_1R>
    </remote_servers>
    <zookeeper>
        <node>
            <host>clickhouse-keeper-01</host>
            <port>9181</port>
        </node>
        <node>
            <host>clickhouse-keeper-02</host>
            <port>9181</port>
        </node>
        <node>
            <host>clickhouse-keeper-03</host>
            <port>9181</port>
        </node>
    </zookeeper>
    <macros>
        <shard>01</shard>
        <replica>01</replica>
        <cluster>cluster_1S_2R</cluster>
        --Макросы для второго кластера 
        <shard_2s>01</shard_2s>
        <replica_2s>01</replica_2s>
        <cluster2>cluster_2S_1R</cluster2>
    </macros>
</clickhouse>
    В данной конфигурации описано два кластера. Первый кластер (cluster_1S_2R) из предыдущего домашнего задания, имеет один шард и две реплики. Второй кластер cluster_2S_1R распределенный (дистрибутивный) имеет 2 шарда и по одной реплики.

2. Создаем локальные и дистриьутивную таблицы на распределенном кластере



CREATE TABLE default.table_distr on cluster cluster_2S_1R
(

    `id` UInt8
)
ENGINE = Distributed('cluster_2S_1R',
 'default',
 'table_local',
 rand());

 CREATE TABLE default.table_local on cluster cluster_2S_1R
(

    `id` UInt8
)
ENGINE = MergeTree
ORDER BY tuple()
SETTINGS index_granularity = 8192;
[1.png]

3.  SELECT *,hostName(),_shard_num from `default`.table_distr
[2.png]

4.   SELECT * FROM system.clusters;
[3.png]

P.S В качестве keeper использовал clickhouse-keeper c 3 отдельными нодами в контейнерах

настройки одной из нод:

<clickhouse replace="true">
    <logger>
        <level>information</level>
        <log>/var/log/clickhouse-keeper/clickhouse-keeper.log</log>
        <errorlog>/var/log/clickhouse-keeper/clickhouse-keeper.err.log</errorlog>
        <size>1000M</size>
        <count>3</count>
    </logger>
    <listen_host>0.0.0.0</listen_host>


<keeper_server>
    <tcp_port>9183</tcp_port>
    <server_id>3</server_id>
    <log_storage_path>/var/lib/clickhouse/coordination/log</log_storage_path>
    <snapshot_storage_path>/var/lib/clickhouse/coordination/snapshots</snapshot_storage_path>
    <coordination_settings>
        <operation_timeout_ms>10000</operation_timeout_ms>
        <session_timeout_ms>30000</session_timeout_ms>
        <raft_logs_level>warning</raft_logs_level>
    </coordination_settings>
    <raft_configuration>
        <server>
            <id>1</id>
            <hostname>clickhouse-keeper-01</hostname>
            <port>9234</port>
        </server>
        <server>
            <id>2</id>
            <hostname>clickhouse-keeper-02</hostname>
            <port>9234</port>
        </server>
        <server>
            <id>3</id>
            <hostname>clickhouse-keeper-03</hostname>
            <port>9234</port>
        </server>
    </raft_configuration>
</keeper_server>
</clickhouse>
