#pragma once

#include <vector>
#include <cstring>
#include <stdexcept>

class Buffer
{
private:
    std::vector<uint8_t> data;
    size_t cursor = 0;
    size_t size_ = 0;


public:
    Buffer(size_t initial_size = 1024) : data(initial_size) {}


    Buffer(const void *initial_data, size_t size) : data(size)
    {
        memcpy(data.data(), initial_data, size);
    }
    void setPosition(size_t position)
    {
        cursor = position;
    } 
    long getPosition()
    {
        return (long)cursor;
    }

    // Write methods
    void writeByte(uint8_t value)
    {
        ensureSpace(sizeof(value));
        data[cursor++] = value;
        size_ += sizeof(value);
    }

    void writeShort(int16_t value)
    {
        ensureSpace(sizeof(value));
        memcpy(&data[cursor], &value, sizeof(value));
        cursor += sizeof(value);
        size_ += sizeof(value);
    }

    void writeUShort(uint16_t value)
    {
        ensureSpace(sizeof(value));
        memcpy(&data[cursor], &value, sizeof(value));
        cursor += sizeof(value);
        size_ += sizeof(value);
    }

    void writeInt(int32_t value)
    {
        ensureSpace(sizeof(value));
        memcpy(&data[cursor], &value, sizeof(value));
        cursor += sizeof(value);
        size_ += sizeof(value);
    }

    void writeLong(int64_t value)
    {
        ensureSpace(sizeof(value));
        memcpy(&data[cursor], &value, sizeof(value));
        cursor += sizeof(value);
        size_ += sizeof(value);
    }

    void writeBytes(const void *buf, size_t size)
    {
        ensureSpace(size);
        memcpy(&data[cursor], buf, size);
        cursor += size;
        size_ += size;
    }

    // Read methods
    uint8_t readByte()
    {
        checkRead(sizeof(uint8_t));
        return data[cursor++];
    }

    int16_t readShort()
    {
        checkRead(sizeof(int16_t));
        int16_t value;
        memcpy(&value, &data[cursor], sizeof(value));
        cursor += sizeof(value);
        return value;
    }

    uint16_t readUShort()
    {
        checkRead(sizeof(uint16_t));
        uint16_t value;
        memcpy(&value, &data[cursor], sizeof(value));
        cursor += sizeof(value);
        return value;
    }


    int32_t readInt()
    {
        checkRead(sizeof(int32_t));
        int32_t value;
        memcpy(&value, &data[cursor], sizeof(value));
        cursor += sizeof(value);
        return value;
    }

    int64_t readLong()
    {
        checkRead(sizeof(int64_t));
        int64_t value;
        memcpy(&value, &data[cursor], sizeof(value));
        cursor += sizeof(value);
        return value;
    }

    void readBytes(void *buf, size_t size)
    {
        checkRead(size);
        memcpy(buf, &data[cursor], size);
        cursor += size;
    }



    
    size_t size() const
    {
        return  size_;
    }

    const uint8_t *getData() const
    {
        return data.data();
    }

    bool hasRemaining() const
    {
        return cursor < cursor;
    }

private:
    void ensureSpace(size_t additionalSize)
    {
        if (cursor + additionalSize > data.size())
        {
            data.resize((cursor + additionalSize) * 2);
        }
    }

    void checkRead(size_t size)
    {
        if (cursor + size > size_)
        {
            throw std::runtime_error("Buffer underflow ( position:"+ std::to_string(cursor) + " size:  " + std::to_string(size_));
        }
    }
};