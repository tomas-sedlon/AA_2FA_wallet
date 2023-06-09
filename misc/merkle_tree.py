from merkly.mtree import MerkleTree

# create a Merkle Tree
mtree = MerkleTree(['a', 'b', 'c', 'd'])

print(mtree)
print(mtree.root)