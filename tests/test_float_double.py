#!/usr/bin/env python
#
# SPDX-FileCopyrightText: 2026 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0
#
import io
import struct
import unittest

from esp_idf_nvs_partition_gen.nvs_partition_gen import InputError, NVS, Page


class FloatDoubleEncodingTests(unittest.TestCase):
    def image(self, entries):
        output = io.BytesIO()
        with NVS(output, 0x3000, Page.VERSION2) as nvs:
            nvs.write_namespace('storage')
            for key, encoding, value in entries:
                nvs.write_entry(key, value, encoding)
        return output.getvalue()

    def entry(self, data, index):
        offset = Page.FIRST_ENTRY_OFFSET + index * Page.SINGLE_ENTRY_SIZE
        return data[offset:offset + Page.SINGLE_ENTRY_SIZE]

    def test_float_and_double_use_firmware_type_codes(self):
        data = self.image([
            ('count', 'u8', '7'),
            ('pi', 'float', '3.5'),
            ('e', 'double', '2.5'),
        ])
        # Namespace is entry 0. The following entries keep the integer path and add IEEE 754.
        integer = self.entry(data, 1)
        single = self.entry(data, 2)
        double = self.entry(data, 3)
        self.assertEqual(integer[1], Page.U8)
        self.assertEqual(integer[24], 7)
        self.assertEqual(single[1], Page.FLOAT)
        self.assertEqual(struct.unpack_from('<f', single, 24)[0], 3.5)
        self.assertEqual(double[1], Page.DOUBLE)
        self.assertEqual(struct.unpack_from('<d', double, 24)[0], 2.5)

    def test_nan_is_rejected(self):
        with self.assertRaises(InputError):
            self.image([('bad', 'float', 'nan')])
        with self.assertRaises(InputError):
            self.image([('bad', 'double', 'NaN')])

    def test_out_of_range_is_rejected(self):
        with self.assertRaises(InputError):
            self.image([('big', 'float', '1e39')])

    def test_underflow_to_zero_is_rejected(self):
        with self.assertRaises(InputError):
            self.image([('tiny', 'float', '1e-50')])

    def test_infinity_is_accepted(self):
        data = self.image([('inf', 'float', 'inf')])
        self.assertEqual(struct.unpack_from('<f', self.entry(data, 1), 24)[0], float('inf'))


if __name__ == '__main__':
    unittest.main()
