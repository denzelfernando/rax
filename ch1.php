#!/usr/bin/php
<?php
require 'vendor/autoload.php';
use OpenCloud\Rackspace;

//Globals
$number_of_server = 3;
$imageId='70d38a32-5f63-45df-a0e7-7e06fc89370a'; //centos
$flavorId='2'; //512MB standard

$config = parse_ini_file('config.ini',true);

//prepare sdk    
$client = new Rackspace(Rackspace::US_IDENTITY_ENDPOINT, array(
    'username' => $config['auth']['username'],
    'apiKey'   => $config['auth']['api_key']
));

//set region
$service = $client->computeService(null, 'SYD');

for ($index = 1; $index <= $number_of_server; $index++) {
    $name =  "web$index";
    
    $server = $service->server();
    
    //Spawn
    echo "Creating The server : {$name}\n";
    $response = $server->create(array(
        'name'     => $name,
        'imageId'  => $imageId,
        'flavorId' => $flavorId
    ));
    
    //Wait till it comes up
    while ($server->status != 'ACTIVE')
    {
        echo "Waiting for the server to become active: {$name} ......... \n";
        $server->waitFor('ACTIVE', 600);
    }
    
    $public_ip_v4=$server->addresses->public[0]->addr;
    echo sprintf("Server Instance Created Name: <%s>, Public IP: <%s>, Secret: <%s> \n", $name, $public_ip_v4, $server->adminPass);
    
    //Bill Guard
    $server->delete();
    
}


?>