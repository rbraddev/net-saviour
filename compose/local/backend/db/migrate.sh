#!/bin/bash

edgedb create-migration --non-interactive --allow-unsafe
edgedb migrate