package com.cse327project.pitlessbucket.file_manager.presentation.upload

import android.net.Uri
import com.cse327project.pitlessbucket.core.data.data_source.UploadResponse

data class FileUploadState(
    val selectedFileUri: Uri? = null,
    val isUploading: Boolean = false,
    val error: String? = null,
    val uploadResponse: UploadResponse? = null
)

