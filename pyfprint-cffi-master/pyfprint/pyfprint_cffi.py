from cffi import FFI
ffi = FFI()

ffi.cdef("""
struct fp_dscv_dev;

struct fp_minutia {
	int x;
	int y;
	int ex;
	int ey;
	int direction;
	double reliability;
	int type;
	int appearing;
	int feature_id;
	int *nbrs;
	int *ridge_counts;
	int num_nbrs;
};

enum fp_enroll_result {
	FP_ENROLL_COMPLETE = 1,
	FP_ENROLL_FAIL,
	FP_ENROLL_PASS,
	FP_ENROLL_RETRY = 100,
	FP_ENROLL_RETRY_TOO_SHORT,
	FP_ENROLL_RETRY_CENTER_FINGER,
	FP_ENROLL_RETRY_REMOVE_FINGER,
};

enum fp_verify_result {
	FP_VERIFY_NO_MATCH = 0,
	FP_VERIFY_MATCH = 1,
	FP_VERIFY_RETRY = FP_ENROLL_RETRY,
	FP_VERIFY_RETRY_TOO_SHORT = FP_ENROLL_RETRY_TOO_SHORT,
	FP_VERIFY_RETRY_CENTER_FINGER = FP_ENROLL_RETRY_CENTER_FINGER,
	FP_VERIFY_RETRY_REMOVE_FINGER = FP_ENROLL_RETRY_REMOVE_FINGER,
};

int fp_init(void);
void fp_exit(void);
void fp_set_debug(int level);

struct fp_dscv_dev **fp_discover_devs(void);
void fp_dscv_devs_free(struct fp_dscv_dev **devs);
uint32_t fp_dscv_dev_get_devtype(struct fp_dscv_dev *dev);
struct fp_driver *fp_dscv_dev_get_driver(struct fp_dscv_dev *dev);
int fp_dscv_dev_supports_dscv_print(struct fp_dscv_dev *dev, struct fp_dscv_print *print);
int fp_dscv_dev_supports_print_data(struct fp_dscv_dev *dev, struct fp_print_data *print);
uint32_t fp_dscv_print_get_devtype(struct fp_dscv_print *print);
uint16_t fp_dscv_print_get_driver_id(struct fp_dscv_print *print);

struct fp_dev *fp_dev_open(struct fp_dscv_dev *ddev);
void fp_dev_close(struct fp_dev *dev);
int fp_dev_supports_print_data(struct fp_dev *dev, struct fp_print_data *data);
uint32_t fp_dev_get_devtype(struct fp_dev *dev);
struct fp_driver *fp_dev_get_driver(struct fp_dev *dev);
int fp_dev_img_capture(struct fp_dev *dev, int unconditional,struct fp_img **image);
int fp_dev_get_img_height(struct fp_dev *dev);
int fp_dev_get_img_width(struct fp_dev *dev);
int fp_dev_get_nr_enroll_stages(struct fp_dev *dev);
int fp_dev_supports_dscv_print(struct fp_dev *dev, struct fp_dscv_print *print);
int fp_dev_supports_identification(struct fp_dev *dev);
int fp_dev_supports_imaging(struct fp_dev *dev);

uint16_t fp_driver_get_driver_id(struct fp_driver *drv);
const char *fp_driver_get_full_name(struct fp_driver *drv);
const char *fp_driver_get_name(struct fp_driver *drv);

int fp_enroll_finger_img(struct fp_dev *dev, struct fp_print_data **print_data, struct fp_img **img);
int fp_verify_finger_img(struct fp_dev *dev, struct fp_print_data *enrolled_print, struct fp_img **img);
int fp_identify_finger_img(struct fp_dev *dev, struct fp_print_data **print_gallery, size_t *match_offset, struct fp_img **img);

int fp_print_data_delete(struct fp_dev *dev, enum fp_finger finger);
int fp_print_data_from_dscv_print(struct fp_dscv_print *print, struct fp_print_data **data);
uint32_t fp_print_data_get_devtype(struct fp_print_data *data);
uint16_t fp_print_data_get_driver_id(struct fp_print_data *data);
int fp_print_data_load(struct fp_dev *dev, enum fp_finger finger, struct fp_print_data **data);
int fp_print_data_save(struct fp_print_data *data, enum fp_finger finger);
size_t fp_print_data_get_data(struct fp_print_data *data, unsigned char **ret);
struct fp_print_data *fp_print_data_from_data(unsigned char *buf, size_t buflen);
void fp_print_data_free(struct fp_print_data *data);

void fp_img_standardize(struct fp_img *img);
struct fp_minutia **fp_img_get_minutiae(struct fp_img *img, int *nr_minutiae);
int fp_img_save_to_file(struct fp_img *img, char *path);
struct fp_img *fp_img_binarize(struct fp_img *img);
int fp_img_compare_print_data_to_gallery(struct fp_print_data *print, struct fp_print_data **gallery, int match_threshold, size_t *match_offset);
int fp_img_get_height(struct fp_img *img);
int fp_img_get_width(struct fp_img *img);
unsigned char *fp_img_get_data(struct fp_img *img);
void fp_img_free(struct fp_img *img);

""")

C = ffi.dlopen('fprint')
