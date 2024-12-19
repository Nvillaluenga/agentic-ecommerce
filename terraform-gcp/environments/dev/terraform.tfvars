project_id        = "<PROJECT ID>"
project_number    = "<PROJECT NUMBER>"
region            = "<REGION>" # For example -> us-central1
langfuse_version  = 2 # V3 is not supported with the current terraform script
nextauth_secret   = "<CREATE ONE>" # Generate a new value: `openssl rand -base64 32`
salt              = "<CREATE ONE>" # Generate a new value: `openssl rand -base64 32`
encryption_key    = "<CREATE ONE>" # Generate a new value: `openssl rand -hex 32`
