`include "terminals_defs.v"
`include "dtypes.v"

module pack_16to8
   #(parameter PIXEL_WIDTH=10)
  (
   input clk,
   input resetb,
   input enable,

   input dvi,
   input [`DTYPE_WIDTH-1:0] dtypei,
   input [15:0] datai,

   output reg dvo,
   output reg [`DTYPE_WIDTH-1:0] dtypeo,
   output reg [15:0] datao,
   output reg [15:0] frame_count
   );

   reg    	packing_phase;
   reg 		enable_s, enable_ss;
   reg [1:0] 	state;
   reg [15:0] 	datai_s;
   parameter STATE_IDLE=0, STATE_FRAME_DATA=2, STATE_HEADER_DATA=3;
   reg [5:0] 	header_addr;
   
   always @(posedge clk or negedge resetb) begin
      if(!resetb) begin
	 packing_phase <= 0;
	 enable_s  <= 0;
	 enable_ss <= 0;
	 state    <= STATE_IDLE;
	 datai_s  <= 0;
	 header_addr <= 0;
	 frame_count <= 0;
	 
      end else begin
	 enable_s <= enable;

	 if(dvi && dtypei == `DTYPE_FRAME_START) begin
	    state <= STATE_FRAME_DATA;
	    enable_ss <= enable_s;
	    frame_count <= frame_count + 1;
	 end else if(dvi && dtypei == `DTYPE_HEADER_START) begin
	    state <= STATE_HEADER_DATA;
	 end else if(dvi && (dtypei == `DTYPE_FRAME_END || dtypei == `DTYPE_HEADER_END)) begin
	    state <= STATE_IDLE;
	 end
	 
	 
	 dtypeo <= dtypei;
	 if(enable_ss && state == STATE_FRAME_DATA) begin
	    if(dvi && |(dtypei & `DTYPE_PIXEL_MASK)) begin
	           packing_phase <= packing_phase + 1;
               case(packing_phase)
                 0: begin
                    datao[7:0] <= datai[PIXEL_WIDTH-1:PIXEL_WIDTH-8];
                    dvo <= 0;
                 end
                 1: begin
                    datao[15:8] <= datai[PIXEL_WIDTH-1:PIXEL_WIDTH-8];
		            dvo <= 1;
                 end
               endcase
	    end else begin
	       dvo <= dvi;
	       datao <= datai;
	    end
	    header_addr   <= 0;

	 end else if(enable_ss && state == STATE_HEADER_DATA) begin
	    if(dvi && dtypei == `DTYPE_HEADER) begin
	      header_addr <= header_addr + 1;
	    end

	    if(header_addr == `Image_image_type) begin
	       datao <= (datai & 16'hFFE0) | 16'h0010;
	    end else begin
	       datao <= datai;
	    end

	    dvo <= dvi;
	    packing_phase <= 0;
	    
	 end else begin
	    header_addr   <= 0;
	    packing_phase <= 0;
	    dvo <= dvi;
	    datao <= datai;
	 end
      end
   end
endmodule
