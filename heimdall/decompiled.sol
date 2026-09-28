// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

/// @title            Decompiled Contract
/// @author           Jonathan Becker <jonathan@jbecker.dev>
/// @custom:version   heimdall-rs v0.9.2
///
/// @notice           This contract was decompiled using the heimdall-rs decompiler.
///                     It was generated directly by tracing the EVM opcodes from this contract.
///                     As a result, it may not compile or even be valid solidity code.
///                     Despite this, it should be obvious what each function does. Overall
///                     logic should have been preserved throughout decompiling.
///
/// @custom:github    You can find the open-source decompiler here:
///                       https://heimdall.rs

contract DecompiledContract {
    mapping(bytes32 => bytes32) storage_map_c;
    mapping(bytes32 => bytes32) storage_map_d;
    address public getOwner;
    uint256 store_b;
    
    
    /// @custom:selector    0x2686ecea
    /// @custom:signature   getServerURL() public view returns (bytes memory)
    function getServerURL() public view returns (bytes memory) {
        if (store_b) {
            if (store_b - ((store_b / 0x02) < 0x20)) {
                uint256 var_c = var_c + (0x20 + (((0x1f + (store_b / 0x02)) / 0x20) * 0x20));
                if (store_b) {
                    if (store_b - ((store_b / 0x02) < 0x20)) {
                        if (!store_b / 0x02) {
                            if (0x1f < (store_b / 0x02)) {
                                var_a = 0x01;
                                if ((0x20 + var_c) + (store_b / 0x02) > (0x20 + (0x20 + var_c))) {
                                    return abi.encodePacked((var_c + 0x20) - var_c, var_c.length);
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    /// @custom:selector    0xd75d1ba6
    /// @custom:signature   Unresolved_d75d1ba6(uint256 arg0, uint0 arg1) public payable
    /// @param              arg0 ["uint256", "bytes32", "int256"]
    /// @param              arg1 ["uint0", "bytes0", "int0"]
    function Unresolved_d75d1ba6(uint256 arg0, uint0 arg1) public payable {
        require(!arg0 > 0xffffffffffffffff);
        require(!(arg0) > 0xffffffffffffffff);
        require(address(msg.sender) == (address(getOwner / 0x01)), "Not owner");
        require(arg0 > 0, "URL too long");
        require(arg0 < 0x0200, "URL too long");
        require(!(arg0 > 0xffffffffffffffff), "Empty URL");
        require(bytes1(store_b), "Empty URL");
        require(bytes1(store_b) - ((store_b / 0x02) < 0x20), "Empty URL");
        require(!((store_b / 0x02) > 0x1f), "Empty URL");
        var_f = 0x01;
        require(!(arg0 < 0x20), "Empty URL");
        require(!(keccak256(var_f) + ((arg0 + 0x1f) / 0x20) < (keccak256(var_f) + (((store_b / 0x02) + 0x1f) / 0x20))), "Empty URL");
        require((arg0 > 0x1f) == 0x01, "Empty URL");
        var_f = 0x01;
        require(!(0 < (uint248(arg0))), "Empty URL");
        require(!(uint248(arg0) < (arg0)), "Empty URL");
        storage_map_d[var_f] = ((arg0 + 0x20) + 0) & (~(0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff >> (0x08 * (bytes1(arg0)))));
        store_b = (arg0 * 0x02) + 0x01;
        store_b = (arg0 * 0x02) + 0x01;
        require(!(arg0), "Empty URL");
        store_b = (((arg0 + 0x20) + 0) & (~(0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff >> (0x08 * (arg0))))) | (0x02 * (arg0));
        store_b = (0 & (~(0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff >> (0x08 * (arg0))))) | (0x02 * (arg0));
    }
    
    /// @custom:selector    0xf2fde38b
    /// @custom:signature   transferOwnership(address arg0) public payable
    /// @param              arg0 ["address", "uint160", "bytes20", "int160"]
    function transferOwnership(address arg0) public payable {
        require(arg0 == (address(arg0)));
        require(address(msg.sender) == (address(getOwner / 0x01)), "Not owner");
        require(address(arg0) - 0, "Zero address");
        getOwner = (address(arg0) * 0x01) | (uint96(getOwner));
    }
}