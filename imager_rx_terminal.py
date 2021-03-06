import nitro, os
from nitro import DeviceInterface, Terminal, Register, SubReg

di = DeviceInterface(
    name="IMAGER_RX",
    comment="""These are the terminals common control an Imager receiver.""",
    terminal_list = [
        Terminal(
            name="ImagerRx",
            regAddrWidth=8,
            regDataWidth=16,
            comment="Controls imager receiver",
            register_list = [
                Register(
                    name="mode",
                    mode="write",
                    shadow=True,
                    subregs = [
                        SubReg(name="test_pat",     width=1, init=0, comment="0: normal mode. 1: enable test pattern substitution"),
                        SubReg(name="left_justify", width=1, init=0, comment="0: right justified data. 1: left justified data stream"),
                        ],
                    ),
                Register(
                    name="frame_count",
                    comment="Count of number of frames",
                    type="int",
                    mode="read",
                    width=16,
                    ),
                Register(
                    name="num_rows",
                    comment="Number of rows in last collected image",
                    type="int",
                    mode="read",
                    width=16,
                    ),
                Register(
                    name="num_cols",
                    comment="number of columns in last collected image",
                    type="int",
                    mode="read",
                    width=16,
                    ),
                Register(
                    name="clks_per_frame",
                    comment="Number of clock cycles in last frame.",
                    type="int",
                    mode="read",
                    width=32,
                    ),
                Register(
                    name="clks_per_row",
                    comment="Number of clock cycles in one row.",
                    type="int",
                    mode="read",
                    width=16,
                    ),
                ],
            ),
        Terminal(
            name="Image",
            regAddrWidth=16,
            regDataWidth=16,
            addr=771,
            comment="Image header and data Terminal",
            register_list = [
                Register(
                    name="frame_start",
                    comment="Header sync word.",
                    type="int",
                    mode="read",
                    width=32,
                    init=0xFFFFFFFE,
                    ),
                Register(
                    name="frame_length",
                    comment="Number of bytes in this frame, including the header.",
                    type="int",
                    mode="read",
                    width=30,
                    init=0,
                    ),
                Register(
                    name="imageHeaderVersion",
                    comment="Image Header version used to capture this image",
                    type="int",
                    mode="read",
                    width=16,
                    init=2,
                    ),
                Register(
                    name="num_rows",
                    comment="Number of rows read from imager",
                    type="int",
                    mode="read",
                    width=16,
                    init=0,
                    ),
                Register(
                    name="num_cols",
                    comment="Number of columns read from imager",
                    type="int",
                    mode="read",
                    width=16,
                    init=0,
                    ),
                Register(
                    name="frame_count",
                    comment="Number of frames that the imager has produced.  You can use this to know if any frames clocked from the image sensor have been dropped.",
                    type="int",
                    mode="read",
                    width=16,
                    init=0,
                    ),
                Register(
                    name="clks_per_frame",
                    comment="Number of clock cycles measured in this frame. Can be used calculate the frame rate and/or integration time.",
                    type="int",
                    mode="read",
                    width=32,
                    init=0,
                    ),
                Register(
                    name="clks_per_row",
                    comment="Number of clock cycles measured per row.",
                    type="int",
                    mode="read",
                    width=16,
                    init=0,
                    ),
                Register(
                    name="checksum",
                    comment="Checksum received by FPGA.",
                    type="int",
                    mode="read",
                    width=16,
                    init=0,
                    ),
                Register(
                    name="image_type",
                    comment="Type of image",
                    type="int",
                    mode="read",
                    sub_regs = [
                        SubReg(name="color", width=4, valuemap={"Mono":0, "Bayer":1}),
                        SubReg(name="packed", width=1),
                        ]
                    ),
                Register(
                    name="flags",
                    width=16,
                    init=0,
                    mode="read",
                    type="int",
                    comment="Flags. This register is hardware specific and gets sampled at the start of every frame.",
                    addr=15,
                    ),
                Register(
                    name="image_data",
                    addr=32,
                    comment="Image data",
                    type="int",
                    mode="read",
                    width=16,
                    init=0,
                    ),
                ],
            ),
        Terminal(
            name="LookupMap",
            regAddrWidth=16,
            regDataWidth=16,
            comment="""
                Write only terminal control the gamma lookup table.,
                This terminal takes PIXEL_WIDTH bits of data from each
                di_write.  So each lookup value should be packed into whatever
                size data type your write bus is. (16 or 32 bits)
                """
            )
         ],
    )
